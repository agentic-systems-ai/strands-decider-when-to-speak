"""LLM wrapper (Bedrock Converse or local ollama): disk cache, structured output, prompt caching.

The provider comes from LLM_PROVIDER (see providers.py). Every response is cached under
data/cache/llm/<sha256>.json keyed by (provider, model, system, messages, tool schema), so
reruns are free and deterministic.
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from . import providers

CACHE_DIR = Path(os.environ.get("LLM_CACHE_DIR", "data/cache/llm"))


def main_model(prov: str | None = None) -> str:
    return providers.model_id("main", prov)


class LLM:
    def __init__(self, model_id: str | None = None, region: str | None = None,
                 cache_dir: Path = CACHE_DIR, max_retries: int = 6, provider: str | None = None):
        self.provider = providers.provider(provider)
        self.model_id = model_id or main_model(self.provider)
        self._br = None
        if self.provider == "bedrock":
            import boto3
            from botocore.config import Config

            self._br = boto3.client("bedrock-runtime", region_name=region or os.environ.get("AWS_REGION"),
                                    config=Config(read_timeout=300, retries={"max_attempts": 2}))
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_retries = max_retries
        self.usage = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0, "calls": 0, "hits": 0}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ core

    def _key(self, payload: dict[str, Any]) -> Path:
        h = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        return self.cache_dir / h[:2] / f"{h}.json"

    def converse(self, system: list[str] | str, user: str, *, tool: dict | None = None,
                 max_tokens: int = 2048, temperature: float = 1.0, salt: str = "") -> dict[str, Any]:
        """One Converse call. `system` blocks are joined with a cache point after them.

        `salt` makes otherwise-identical prompts cache separately (e.g. a re-render retry).
        """
        sys_blocks = [system] if isinstance(system, str) else list(system)
        payload = {"provider": self.provider, "model": self.model_id, "system": sys_blocks, "user": user, "tool": tool,
                   "max_tokens": max_tokens, "temperature": temperature, "salt": salt}
        path = self._key(payload)
        if path.exists():
            with self._lock:
                self.usage["hits"] += 1
            return json.loads(path.read_text(encoding="utf-8"))

        if self.provider == "ollama":
            r = providers.ollama_chat(self.model_id, "\n\n".join(sys_blocks), user,
                                      schema=tool["inputSchema"]["json"] if tool else None,
                                      max_tokens=max_tokens, temperature=temperature)
            return self._store(path, {"text": r["text"], "tool_input": r["json"], "usage": r["usage"]})

        req: dict[str, Any] = {
            "modelId": self.model_id,
            "system": [{"text": s} for s in sys_blocks]
                      + ([{"cachePoint": {"type": "default"}}] if providers.bedrock_supports_cache_point(self.model_id) else []),
            "messages": [{"role": "user", "content": [{"text": user}]}],
            "inferenceConfig": {"maxTokens": max_tokens, "temperature": temperature},
        }
        if extra := providers.bedrock_extra_fields(self.model_id):
            req["additionalModelRequestFields"] = extra
        if tool:
            req["toolConfig"] = {"tools": [{"toolSpec": tool}],
                                 "toolChoice": {"tool": {"name": tool["name"]}}}
        resp = self._call(req)
        out = {"text": "", "tool_input": None, "usage": resp.get("usage", {})}
        for block in resp["output"]["message"]["content"]:
            if "text" in block:
                out["text"] += block["text"]
            if "toolUse" in block:
                out["tool_input"] = block["toolUse"]["input"]
        return self._store(path, out)

    def _store(self, path: Path, out: dict[str, Any]) -> dict[str, Any]:
        u = out["usage"]
        with self._lock:
            self.usage["calls"] += 1
            self.usage["input"] += u.get("inputTokens", 0)
            self.usage["output"] += u.get("outputTokens", 0)
            self.usage["cache_read"] += u.get("cacheReadInputTokens", 0)
            self.usage["cache_write"] += u.get("cacheWriteInputTokens", 0)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
        return out

    def _call(self, req: dict[str, Any]) -> dict[str, Any]:
        from botocore.exceptions import ClientError

        for attempt in range(self.max_retries):
            try:
                return self._br.converse(**req)
            except ClientError as e:
                code = e.response.get("Error", {}).get("Code", "")
                if code in ("ThrottlingException", "ServiceUnavailableException",
                            "ModelNotReadyException") and attempt < self.max_retries - 1:
                    time.sleep(min(30, 2 ** attempt))
                    continue
                raise
        raise RuntimeError("unreachable")

    # ------------------------------------------------------------- helpers

    def structured(self, system: list[str] | str, user: str, model: type[BaseModel], *,
                   name: str = "submit", description: str = "Submit the result.",
                   **kw: Any) -> BaseModel:
        """Force a tool call whose input schema is `model`'s JSON schema; validate it."""
        tool = {"name": name, "description": description,
                "inputSchema": {"json": model.model_json_schema()}}
        for salt in ("", "retry"):  # gpt-oss occasionally returns an empty reply; ask once more
            out = self.converse(system, user, tool=tool, salt=salt, **kw)
            data = out["tool_input"]
            if not data:
                # gpt-oss sometimes answers a forced tool call with the JSON as plain text.
                text = out["text"]
                start, end = text.find("{"), text.rfind("}")
                if start != -1 and end > start:
                    try:
                        data = json.loads(text[start:end + 1])
                    except json.JSONDecodeError:
                        data = None
            if data:
                break
        return model.model_validate(data or {})

    def text(self, system: list[str] | str, user: str, **kw: Any) -> str:
        return self.converse(system, user, **kw)["text"].strip()
