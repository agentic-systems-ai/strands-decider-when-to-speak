"""Which LLM backs the agent, the recap and the LLM-judge baseline: local ollama or Bedrock.

    LLM_PROVIDER=ollama   (default)  OLLAMA_HOST=http://127.0.0.1:11434
                                     OLLAMA_MODEL_MAIN=qwen3:8b  OLLAMA_MODEL_BASELINE=qwen3:8b
                                     OLLAMA_NUM_CTX=8192
    LLM_PROVIDER=bedrock             AWS_REGION, BEDROCK_MODEL_MAIN, BEDROCK_MODEL_BASELINE

ollama is for prototyping and validation on the dev box; Bedrock is the real experiment.
Model ids are never hard-coded for Bedrock (they come from the environment).
"""

from __future__ import annotations

import os
from typing import Any, Literal

Provider = Literal["ollama", "bedrock"]
Role = Literal["main", "baseline"]

OLLAMA_DEFAULT_MODEL = "qwen3:8b"


def provider(name: str | None = None) -> Provider:
    p = (name or os.environ.get("LLM_PROVIDER", "ollama")).lower()
    if p not in ("ollama", "bedrock"):
        raise ValueError(f"LLM_PROVIDER must be 'ollama' or 'bedrock', not {p!r}")
    return p  # type: ignore[return-value]


def ollama_host() -> str:
    return os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")


def ollama_num_ctx() -> int:
    """One context size for every ollama call. Left unset, ollama sizes it per request from free
    VRAM, so calls alternate between sizes, each switch reloads the model, and long prompts get
    silently truncated at 4096."""
    return int(os.environ.get("OLLAMA_NUM_CTX", "8192"))


def bedrock_extra_fields(mid: str) -> dict[str, Any]:
    """Converse `additionalModelRequestFields` for a Bedrock model id. gpt-oss reasons before
    answering and bills it as output; low effort (BEDROCK_REASONING_EFFORT) cuts that ~7x."""
    if "gpt-oss" in mid:
        return {"reasoning_effort": os.environ.get("BEDROCK_REASONING_EFFORT", "low")}
    return {}


def bedrock_supports_cache_point(mid: str) -> bool:
    return "anthropic" in mid or "nova" in mid


def model_id(role: Role = "main", prov: str | None = None) -> str:
    if provider(prov) == "bedrock":
        return os.environ[f"BEDROCK_MODEL_{role.upper()}"]
    return os.environ.get(f"OLLAMA_MODEL_{role.upper()}", OLLAMA_DEFAULT_MODEL)


def strands_model(role: Role = "main", *, prov: str | None = None, model: str | None = None,
                  max_tokens: int = 600, temperature: float | None = None) -> Any:
    """A Strands model for the configured provider."""
    mid = model or model_id(role, prov)
    if provider(prov) == "bedrock":
        from botocore.config import Config
        from strands.models import BedrockModel

        kw: dict[str, Any] = {"temperature": temperature} if temperature is not None else {}
        # A stalled stream otherwise waits the full 120 s default and then fails the run.
        kw["boto_client_config"] = Config(read_timeout=60, connect_timeout=10,
                                          retries={"max_attempts": 4, "mode": "standard"})
        if extra := bedrock_extra_fields(mid):
            kw["additional_request_fields"] = extra
        cls = _GptOssBedrockModel if "gpt-oss" in mid else BedrockModel
        return cls(model_id=mid, region_name=os.environ.get("AWS_REGION"), max_tokens=max_tokens, **kw)
    from strands.models.ollama import OllamaModel

    kw = {"temperature": temperature} if temperature is not None else {}
    # qwen3 thinks by default; the agent's tool calls don't need it and it costs seconds per wake.
    return OllamaModel(ollama_host(), model_id=mid, max_tokens=max_tokens, keep_alive="10m",
                       options={"num_ctx": ollama_num_ctx()}, additional_args={"think": False}, **kw)


def ollama_chat(model: str, system: str, user: str, *, schema: dict | None = None,
                max_tokens: int = 2048, temperature: float = 0.7) -> dict[str, Any]:
    """One ollama chat call. With `schema`, the reply is constrained to that JSON schema.

    Returns {"text", "json" (parsed when schema is given), "usage": {"inputTokens", "outputTokens"}}.
    """
    import json

    import ollama

    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    resp = ollama.Client(host=ollama_host()).chat(
        model=model, messages=msgs, format=schema, think=False, keep_alive="10m",
        options={"num_predict": max_tokens, "temperature": temperature, "num_ctx": ollama_num_ctx()})
    text = resp.message.content or ""
    out: dict[str, Any] = {"text": text, "json": None,
                           "usage": {"inputTokens": resp.prompt_eval_count or 0,
                                     "outputTokens": resp.eval_count or 0}}
    if schema is not None:
        try:
            out["json"] = json.loads(text)
        except json.JSONDecodeError:
            out["json"] = {}
    return out


def _clean_tool_name(name: str) -> str:
    """gpt-oss sometimes leaks its channel markup into the tool name:
    "compose_interjection<|channel|>commentary" -> "compose_interjection"."""
    return name.split("<|", 1)[0].strip()


try:
    from strands.models import BedrockModel as _BedrockModel

    class _GptOssBedrockModel(_BedrockModel):
        async def stream(self, *args: Any, **kwargs: Any):
            async for event in super().stream(*args, **kwargs):
                tool_use = event.get("contentBlockStart", {}).get("start", {}).get("toolUse")
                if tool_use and "name" in tool_use:
                    tool_use["name"] = _clean_tool_name(tool_use["name"])
                yield event
except ImportError:  # pragma: no cover
    pass
