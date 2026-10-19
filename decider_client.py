"""decider_client.py: the only module that talks to Strands Decider.

Three clients share one interface (`ask(state, questions) -> {key: Decision}`):

- DeciderClient       the real model, over the local HTTP server or in-process
- FakeDeciderClient   scripted answers, for unit tests
- LLMJudgeClient     the same questions answered by an LLM (the baseline): local ollama or Bedrock,
                     per LLM_PROVIDER (BedrockJudgeClient forces Bedrock)

API facts this relies on are recorded in docs/VERIFIED_APIS.md.
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

QType = Literal["noul", "choice", "score"]

DEFAULT_MODEL_ID = os.environ.get(
    "DECIDER_MODEL_ID", "StrandsAgents/strands-decider-2B-qwen3.5-v1-2610"
)
DEFAULT_URL = os.environ.get("DECIDER_URL", "http://127.0.0.1:8099")
DEFAULT_LOG = Path(os.environ.get("DECIDER_LOG", "runs/decisions.jsonl"))


@dataclass(frozen=True)
class Question:
    key: str                 # stable id, e.g. "category"
    qtype: QType
    text: str                # the question prompt
    options: dict[str, str]  # option label -> description (noul: {"true":..., "false":...});
                             # score: ascending order, lowest level first

    def to_wire(self) -> dict[str, Any]:
        """The /v1/systemone question body."""
        if self.qtype == "noul":
            crit = {k: v for k, v in self.options.items() if k in ("true", "false")}
            return {"type": "noul", "instructions": self.text, "criteria": crit or None}
        if self.qtype == "choice":
            return {"type": "choice", "instructions": self.text, "criteria": dict(self.options)}
        return {"type": "score", "instructions": self.text, "criteria": list(self.options.values())}


@dataclass
class Decision:
    key: str
    answer: str              # winning option label
    confidence: float        # probability of the winning option (see VERIFIED_APIS.md)
    probs: dict[str, float]  # per-option probabilities
    margin: float            # top1 - top2 probability
    latency_ms: float        # wall-clock for the batch this came from

    @property
    def p_true(self) -> float:
        """P(true) for a noul question; convenience for policies."""
        return self.probs.get("true", 0.0)


def _decision(key: str, probs: dict[str, float], latency_ms: float) -> Decision:
    ranked = sorted(probs.items(), key=lambda kv: kv[1], reverse=True)
    top = ranked[0]
    second = ranked[1][1] if len(ranked) > 1 else 0.0
    return Decision(key, top[0], top[1], probs, top[1] - second, latency_ms)


def parse_answer(q: Question, ans: dict[str, Any], latency_ms: float) -> Decision:
    """Turn one /v1/systemone answer into a Decision."""
    if ans["type"] == "noul":
        p = float(ans["noul"])
        return _decision(q.key, {"true": p, "false": 1.0 - p}, latency_ms)
    if ans["type"] == "choice":
        return _decision(q.key, {k: float(v) for k, v in ans["probabilities"].items()}, latency_ms)
    # score: the server keys probabilities by level index; map back to our labels.
    labels = list(q.options.keys())
    probs = {labels[int(i)]: float(v) for i, v in ans["probabilities"].items()}
    return _decision(q.key, probs, latency_ms)


class _JsonlLog:
    """Thread-safe JSONL logger shared by all clients."""

    def __init__(self, path: Path | None):
        self.path = path
        self._lock = threading.Lock()
        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, record: dict[str, Any]) -> None:
        if self.path is None:
            return
        line = json.dumps(record, ensure_ascii=False)
        with self._lock, self.path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def state_hash(state: str) -> str:
    return hashlib.sha256(state.encode("utf-8")).hexdigest()[:16]


class _BaseClient:
    backend = "base"

    def __init__(self, log_path: Path | None = DEFAULT_LOG):
        self._log = _JsonlLog(log_path)
        self.last_batch_path = "loop"

    def _record(self, state: str, questions: Sequence[Question], out: dict[str, Decision],
                latency_ms: float, input_tokens: int | None, extra: dict | None = None) -> None:
        self._log.write({
            "ts": time.time(),
            "backend": self.backend,
            "state_hash": state_hash(state),
            "input_tokens": input_tokens,
            "questions": [q.key for q in questions],
            "decisions": {k: {"answer": d.answer, "confidence": round(d.confidence, 4),
                              "probs": {o: round(p, 4) for o, p in d.probs.items()}}
                          for k, d in out.items()},
            "latency_ms": round(latency_ms, 2),
            **(extra or {}),
        })

    def warmup(self) -> None:
        pass

    def ask(self, state: str, questions: Sequence[Question]) -> dict[str, Decision]:
        raise NotImplementedError

    def ask_many(self, items: Sequence[tuple[str, Sequence[Question]]]) -> list[dict[str, Decision]]:
        """Batch several states if the backend supports it; otherwise loop.

        The Decider server takes one state per request (VERIFIED_APIS.md), so every
        backend here loops. `last_batch_path` reports which path was used.
        """
        self.last_batch_path = "loop"
        return [self.ask(s, qs) for s, qs in items]


class DeciderClient(_BaseClient):
    """The real Strands Decider, over HTTP (default) or loaded in-process."""

    backend = "decider"

    def __init__(self, mode: Literal["inproc", "http"] = "http",
                 model_id: str = DEFAULT_MODEL_ID,
                 url: str = DEFAULT_URL, device: str = "cuda",
                 timeout_s: float = 30.0, log_path: Path | None = DEFAULT_LOG):
        super().__init__(log_path)
        self.mode = mode
        self.model_id = model_id
        self.url = url.rstrip("/")
        self.device = device
        self.timeout_s = timeout_s
        self._engine = None
        self._session = None
        if mode == "inproc":
            from strands_decider.infer import load_engine
            self._engine = load_engine(model_id, device=device)
        else:
            import requests
            self._session = requests.Session()

    def health(self) -> dict[str, Any]:
        if self._engine is not None:
            return {"status": "ok", "mode": "inproc", "model": self.model_id, "device": self.device}
        r = self._session.get(f"{self.url}/health", timeout=self.timeout_s)
        r.raise_for_status()
        return r.json()

    def warmup(self) -> None:
        """The first request is slow (~8 s) while kernels compile; pay it at startup."""
        q = Question("warmup", "noul", "Is this a warm-up request?", {})
        for _ in range(2):
            self._call("warm-up state", [q])

    def _call(self, state: str, questions: Sequence[Question]) -> tuple[dict[str, Any], float]:
        body = {"state": state, "questions": {q.key: q.to_wire() for q in questions}}
        t0 = time.perf_counter()
        if self._engine is not None:
            from strands_decider.schema import SystemOneRequest
            payload = self._engine.evaluate(SystemOneRequest(**body)).model_dump()
        else:
            r = self._session.post(f"{self.url}/v1/systemone", json=body, timeout=self.timeout_s)
            if r.status_code >= 400:
                raise RuntimeError(f"decider {r.status_code}: {r.text[:500]}")
            payload = r.json()
        return payload, (time.perf_counter() - t0) * 1000

    def ask(self, state: str, questions: Sequence[Question]) -> dict[str, Decision]:
        if not questions:
            return {}
        payload, ms = self._call(state, questions)
        out = {q.key: parse_answer(q, payload["answers"][q.key], ms) for q in questions}
        self._record(state, questions, out, ms, payload.get("usage", {}).get("input_tokens"),
                     {"server_ms": payload.get("latency_ms")})
        return out


ScriptFn = Callable[[str, Question], dict[str, float] | float | str]


class FakeDeciderClient(_BaseClient):
    """Scripted decisions for unit tests.

    `script(state, question)` may return a probability dict, a float (P(true) for a
    noul), or an option label (probability 1.0). Unscripted questions get the first
    listed non-"true" option, i.e. "false" for nouls.
    """

    backend = "fake"

    def __init__(self, script: ScriptFn | None = None, latency_ms: float = 1.0,
                 log_path: Path | None = None):
        super().__init__(log_path)
        self.script = script
        self.latency_ms = latency_ms
        self.calls: list[tuple[str, list[str]]] = []

    def _probs(self, state: str, q: Question) -> dict[str, float]:
        labels = ["true", "false"] if q.qtype == "noul" else list(q.options)
        v = self.script(state, q) if self.script else None
        if v is None:
            default = "false" if q.qtype == "noul" else labels[0]
            return {lbl: float(lbl == default) for lbl in labels}
        if isinstance(v, dict):
            return {lbl: float(v.get(lbl, 0.0)) for lbl in labels}
        if isinstance(v, (int, float)):
            return {"true": float(v), "false": 1.0 - float(v)}
        return {lbl: float(lbl == v) for lbl in labels}

    def ask(self, state: str, questions: Sequence[Question]) -> dict[str, Decision]:
        self.calls.append((state, [q.key for q in questions]))
        out = {q.key: _decision(q.key, self._probs(state, q), self.latency_ms) for q in questions}
        self._record(state, questions, out, self.latency_ms, None)
        return out


SHORTHAND_CONFIDENCE = 0.9  # judge answered "true" without a confidence


class LLMJudgeClient(_BaseClient):
    """The same typed questions answered by an LLM: the baseline.

    Bedrock uses a forced tool call; ollama uses a JSON-schema-constrained reply. Either way
    the answer is one option label plus a self-reported probability per question. Token
    usage is logged for cost charts.

    provider: "ollama" (default; OLLAMA_HOST, OLLAMA_MODEL_BASELINE, default qwen3:8b) or
    "bedrock" (AWS_REGION, BEDROCK_MODEL_BASELINE); defaults to env LLM_PROVIDER.
    """

    def __init__(self, model_id: str | None = None, region: str | None = None,
                 max_tokens: int = 1024, log_path: Path | None = DEFAULT_LOG, provider: str | None = None):
        super().__init__(log_path)
        self.provider = (provider or os.environ.get("LLM_PROVIDER", "ollama")).lower()
        self.backend = f"{self.provider}_judge"
        if self.provider == "bedrock":
            import boto3
            self.model_id = model_id or os.environ["BEDROCK_MODEL_BASELINE"]
            self._br = boto3.client("bedrock-runtime", region_name=region or os.environ.get("AWS_REGION"))
        elif self.provider == "ollama":
            self.model_id = model_id or os.environ.get("OLLAMA_MODEL_BASELINE", "qwen3:8b")
            self._host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
        else:
            raise ValueError(f"unknown provider {self.provider!r}")
        self.max_tokens = max_tokens
        self.usage = {"input_tokens": 0, "output_tokens": 0, "calls": 0}

    @staticmethod
    def _labels(q: Question) -> list[str]:
        return ["true", "false"] if q.qtype == "noul" else list(q.options)

    def _tool(self, questions: Sequence[Question]) -> dict[str, Any]:
        props = {
            q.key: {
                "type": "object",
                "properties": {
                    "answer": {"type": "string", "enum": self._labels(q)},
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1,
                                   "description": "probability that `answer` is correct"},
                },
                "required": ["answer", "confidence"],
            }
            for q in questions
        }
        return {"toolSpec": {
            "name": "submit_answers",
            "description": "Submit one answer per question.",
            "inputSchema": {"json": {"type": "object", "properties": props,
                                     "required": [q.key for q in questions]}},
        }}

    @staticmethod
    def _prompt(state: str, questions: Sequence[Question]) -> str:
        parts = [f"<state>\n{state}\n</state>\n", "Answer every question about the state above."]
        for q in questions:
            opts = {"true": "the statement holds", "false": "the statement does not hold"} \
                if q.qtype == "noul" else {}
            opts.update(q.options)
            lines = "\n".join(f"  - {k}: {v}" for k, v in opts.items())
            parts.append(f"\n[{q.key}] ({q.qtype}) {q.text}\n{lines}")
        return "\n".join(parts)

    def ask(self, state: str, questions: Sequence[Question]) -> dict[str, Decision]:
        if not questions:
            return {}
        t0 = time.perf_counter()
        tool_input, usage = (self._ask_bedrock if self.provider == "bedrock" else self._ask_ollama)(
            state, questions)
        ms = (time.perf_counter() - t0) * 1000
        self.usage["input_tokens"] += usage.get("inputTokens", 0)
        self.usage["output_tokens"] += usage.get("outputTokens", 0)
        self.usage["calls"] += 1
        out: dict[str, Decision] = {}
        for q in questions:
            labels = self._labels(q)
            a = tool_input.get(q.key) or {}
            if not isinstance(a, dict):
                # Shorthand like {"action_item": "true"}: keep the answer, assume a typical confidence.
                self.usage["shorthand"] = self.usage.get("shorthand", 0) + 1
                a = {"answer": str(a).lower(), "confidence": SHORTHAND_CONFIDENCE}
            answer = a.get("answer") if a.get("answer") in labels else labels[-1]
            try:
                conf = min(1.0, max(0.0, float(a.get("confidence", 0.5))))
            except (TypeError, ValueError):
                conf = 0.5
            rest = (1.0 - conf) / max(1, len(labels) - 1)
            out[q.key] = _decision(q.key, {lbl: conf if lbl == answer else rest for lbl in labels}, ms)
        self._record(state, questions, out, ms, usage.get("inputTokens"),
                     {"model_id": self.model_id, "output_tokens": usage.get("outputTokens")})
        return out

    def _ask_bedrock(self, state: str, questions: Sequence[Question]) -> tuple[dict[str, Any], dict]:
        from when_to_speak.providers import bedrock_extra_fields

        extra = bedrock_extra_fields(self.model_id)
        resp = self._br.converse(
            modelId=self.model_id,
            messages=[{"role": "user", "content": [{"text": self._prompt(state, questions)}]}],
            toolConfig={"tools": [self._tool(questions)],
                        "toolChoice": {"tool": {"name": "submit_answers"}}},
            inferenceConfig={"maxTokens": self.max_tokens},
            **({"additionalModelRequestFields": extra} if extra else {}),
        )
        tool_input: dict[str, Any] = {}
        text = ""
        for block in resp["output"]["message"]["content"]:
            if "toolUse" in block:
                tool_input = block["toolUse"]["input"]
            text += block.get("text", "")
        if not tool_input and "{" in text:
            # gpt-oss sometimes answers a forced tool call with the JSON as plain text.
            try:
                tool_input = json.loads(text[text.find("{"):text.rfind("}") + 1])
            except json.JSONDecodeError:
                pass
        return tool_input, resp.get("usage", {})

    def _ask_ollama(self, state: str, questions: Sequence[Question]) -> tuple[dict[str, Any], dict]:
        import ollama
        from when_to_speak.providers import ollama_num_ctx

        schema = self._tool(questions)["toolSpec"]["inputSchema"]["json"]
        resp = ollama.Client(host=self._host).chat(
            model=self.model_id, think=False, format=schema, keep_alive="10m",
            messages=[{"role": "user", "content": self._prompt(state, questions)
                       + "\n\nReply with the JSON object only."}],
            options={"num_predict": self.max_tokens, "temperature": 0.0, "num_ctx": ollama_num_ctx()})
        try:
            tool_input = json.loads(resp.message.content or "{}")
        except json.JSONDecodeError:
            tool_input = {}
        return tool_input, {"inputTokens": resp.prompt_eval_count or 0, "outputTokens": resp.eval_count or 0}


class BedrockJudgeClient(LLMJudgeClient):
    """LLMJudgeClient pinned to Bedrock."""

    def __init__(self, model_id: str | None = None, region: str | None = None, max_tokens: int = 1024,
                 log_path: Path | None = DEFAULT_LOG):
        super().__init__(model_id, region, max_tokens, log_path, provider="bedrock")


__all__ = [
    "Question", "Decision", "DeciderClient", "FakeDeciderClient", "LLMJudgeClient", "BedrockJudgeClient",
    "parse_answer", "state_hash",
]
