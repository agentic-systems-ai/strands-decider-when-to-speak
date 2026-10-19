"""The intervention inside a real Strands Agent, with a stub model (no AWS, no GPU)."""

from __future__ import annotations

from typing import Any

from decider_client import FakeDeciderClient
from strands import Agent
from strands.models.model import Model

from interjection_policy import (
    InterjectionGate,
    InterjectionIntervention,
    Thresholds,
    TieredPolicy,
    make_interjection_questions,
)


class StubModel(Model):
    """Replies "ok" and records what it was sent."""

    def __init__(self) -> None:
        self.calls: list[list[dict[str, Any]]] = []

    def update_config(self, **kw: Any) -> None: ...

    def get_config(self) -> Any:
        return {}

    def structured_output(self, *a: Any, **kw: Any):  # pragma: no cover
        raise NotImplementedError

    async def stream(self, messages, tool_specs=None, system_prompt=None, **kw):
        self.calls.append([dict(m) for m in messages])
        yield {"messageStart": {"role": "assistant"}}
        yield {"contentBlockStart": {"start": {}}}
        yield {"contentBlockDelta": {"delta": {"text": "ok"}}}
        yield {"contentBlockStop": {}}
        yield {"messageStop": {"stopReason": "end_turn"}}


def _agent():
    fake = FakeDeciderClient(lambda s, q: 0.95 if "broken" in s else 0.05)
    gate = InterjectionGate(fake, make_interjection_questions({"bug_report": "a bug report"}),
                            TieredPolicy({"bug_report": Thresholds(0.8, 0.5)}, dedupe=None))
    seen = []
    handler = InterjectionIntervention(gate, on_result=seen.append)
    model = StubModel()
    return Agent(model=model, interventions=[handler], callback_handler=None), model, seen


def test_silent_ticks_never_call_the_model_and_leave_no_junk():
    agent, model, seen = _agent()
    for msg in ["morning all", "lunch?", "nice weather"]:
        agent(msg)
    assert model.calls == []
    assert len(seen) == 3 and not any(r.wake for r in seen)
    # Strands appends an assistant DENIED message per cancel; the handler strips the
    # previous ones, so at most the latest remains.
    assert sum(m["role"] == "assistant" for m in agent.messages) <= 1


def test_wake_calls_model_with_reason_note_and_valid_history():
    agent, model, seen = _agent()
    agent("hello")
    agent("checkout is broken for EU customers")
    assert len(model.calls) == 1
    sent = model.calls[0]
    texts = [b.get("text", "") for m in sent for b in m["content"]]
    assert any("bug_report" in t and "0.95" in t for t in texts)
    roles = [m["role"] for m in sent]
    assert roles[0] == "user" and all(a != b for a, b in zip(roles, roles[1:]))


class LoopingModel(StubModel):
    """Calls the same tool on every turn and never stops by itself."""

    async def stream(self, messages, tool_specs=None, system_prompt=None, **kw):
        self.calls.append([dict(m) for m in messages])
        n = len(self.calls)
        yield {"messageStart": {"role": "assistant"}}
        yield {"contentBlockStart": {"start": {"toolUse": {"toolUseId": f"t{n}", "name": "note"}}}}
        yield {"contentBlockDelta": {"delta": {"toolUse": {"input": "{}"}}}}
        yield {"contentBlockStop": {}}
        yield {"messageStop": {"stopReason": "tool_use"}}


def test_model_call_cap_ends_a_tool_loop_and_resets_per_wake():
    from strands import tool

    @tool
    def note() -> str:
        """Take a note."""
        return "noted"

    fake = FakeDeciderClient(lambda s, q: 0.95 if "broken" in s else 0.05)
    gate = InterjectionGate(fake, make_interjection_questions({"bug_report": "a bug report"}),
                            TieredPolicy({"bug_report": Thresholds(0.8, 0.5)}, dedupe=None, cooldown_s=0))
    handler = InterjectionIntervention(gate, max_model_calls=3)
    model = LoopingModel()
    agent = Agent(model=model, tools=[note], interventions=[handler], callback_handler=None)
    agent("checkout is broken")
    assert len(model.calls) == 3
    agent.messages.clear()
    agent("checkout is still broken")
    assert len(model.calls) == 6


def test_gpt_oss_tool_name_markup_is_stripped():
    from when_to_speak.providers import _clean_tool_name

    assert _clean_tool_name("compose_interjection<|channel|>commentary") == "compose_interjection"
    assert _clean_tool_name("record_decision") == "record_decision"
