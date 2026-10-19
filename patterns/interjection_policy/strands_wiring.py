"""Wiring the interjection policy into a Strands agent.

Two layers:

- `InterjectionGate.should_wake(state, now)`: framework-free. One Decider call, then
  the policy. Use it directly if you drive your own loop.
- `InterjectionIntervention`: a Strands `InterventionHandler` on `before_invocation`.
  Every stream chunk is sent to the agent as a normal call; the handler denies it
  (no model call, no tokens) unless the policy says SPEAK, in which case it lets the
  call through and appends a note telling the agent *why* it was woken.

Strands specifics (verified against strands-agents 1.60, see docs/VERIFIED_APIS.md):

- On `before_invocation`, `Guide` *cancels* the call (it does not inject text), so the
  wake note is added with `Transform`, which mutates `event.messages`.
- A cancelled invocation appends an assistant "DENIED: ..." message to
  `agent.messages`. Left alone, silent ticks would pile up consecutive assistant
  turns, which Bedrock rejects. The handler strips its own denial messages at the
  start of every invocation.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from decider_client import Decision, Question
from strands.interventions import Deny, InterventionHandler, Proceed, Transform

from .policy import Action, PolicyResult, TieredPolicy, signals_from

DENY_TAG = "[interjection-gate]"
STATE_KEY = "interjection_state"  # invocation_state key carrying a pre-rendered window


@dataclass
class GateResult:
    action: Action
    category: str | None
    confidence: float
    reasons: list[str]
    decisions: dict[str, Decision]
    signals: dict[str, float]
    latency_ms: float
    state: str
    tiers: dict[str, Action] = field(default_factory=dict)

    @property
    def wake(self) -> bool:
        return self.action is Action.SPEAK

    def ticker(self) -> str:
        """`action_item 0.07 · decision_made 0.02 · factual_claim 0.91 -> speak · 118 ms`"""
        parts = [f"{k} {v:.2f}" for k, v in self.signals.items()]
        return " · ".join(parts) + f" -> {self.action.value} · {self.latency_ms:.0f} ms"


DeriveFn = Callable[[dict[str, Decision], dict[str, float]], Mapping[str, float]]


class InterjectionGate:
    """Decider + policy.

    `questions` may be a list or a callable re-built per tick (e.g. add a question only
    while something is pending). `derive` may add signals computed from the decisions
    and your own state, e.g. "the pending question is still unanswered after 2 ticks".
    """

    def __init__(self, decider: Any, questions: Sequence[Question] | Callable[[], Sequence[Question]],
                 policy: TieredPolicy,
                 choice_signals: Mapping[str, tuple[str, str]] | None = None,
                 derive: DeriveFn | None = None):
        self.decider = decider
        self.questions = questions
        self.policy = policy
        self.choice_signals = dict(choice_signals or {})
        self.derive = derive

    def should_wake(self, state: str, now: float | None = None) -> GateResult:
        now = time.monotonic() if now is None else now
        qs = self.questions() if callable(self.questions) else self.questions
        decisions = self.decider.ask(state, qs)
        signals = signals_from(decisions, self.choice_signals)
        if self.derive:
            signals.update(self.derive(decisions, signals))
        res: PolicyResult = self.policy.decide(signals, now)
        latency = max((d.latency_ms for d in decisions.values()), default=0.0)
        return GateResult(res.action, res.category, res.confidence, res.reasons,
                          decisions, signals, latency, state, res.tiers)


def _last_user_text(messages: list[dict[str, Any]] | None) -> str:
    for m in reversed(messages or []):
        if m.get("role") == "user":
            return "\n".join(b["text"] for b in m.get("content", []) if "text" in b)
    return ""


def _is_own_denial(m: dict[str, Any]) -> bool:
    return m.get("role") == "assistant" and any(
        DENY_TAG in b.get("text", "") for b in m.get("content", []))


class InterjectionIntervention(InterventionHandler):
    """`Agent(interventions=[InterjectionIntervention(gate)])`

    The state is taken from `invocation_state["interjection_state"]` if present,
    otherwise from the text of the incoming user message. Each result is passed to
    `on_result` (for tickers, notes and logs) and kept in `last_result`.

    A woken invocation gets at most `max_model_calls` model calls; past that the call is
    denied, which ends the invocation. Small models otherwise keep calling tools until the
    context fills up.
    """

    name = "interjection-policy"

    def __init__(self, gate: InterjectionGate,
                 render_state: Callable[[str], str] | None = None,
                 on_result: Callable[[GateResult], None] | None = None,
                 clock: Callable[[], float] = time.monotonic,
                 max_model_calls: int | None = 4):
        self.gate = gate
        self.render_state = render_state
        self.on_result = on_result
        self.clock = clock
        self.max_model_calls = max_model_calls
        self.last_result: GateResult | None = None
        self.model_calls = 0

    def before_invocation(self, event, **kwargs):
        # Drop the assistant "DENIED" turns our earlier cancellations left behind.
        msgs = event.agent.messages
        msgs[:] = [m for m in msgs if not _is_own_denial(m)]
        self.model_calls = 0

        state = event.invocation_state.get(STATE_KEY) if event.invocation_state else None
        if state is None:
            text = _last_user_text(event.messages)
            state = self.render_state(text) if self.render_state else text

        res = self.gate.should_wake(state, self.clock())
        self.last_result = res
        if self.on_result:
            self.on_result(res)

        if not res.wake:
            return Deny(reason=f"{DENY_TAG} {res.action.value}: {'; '.join(res.reasons)}")

        if res.category is None:  # a gate that wakes on everything has nothing to report
            return Proceed()
        note = (f"{DENY_TAG} You were woken because the decision model flagged "
                f"'{res.category}' with confidence {res.confidence:.2f}.")

        def add_note(e) -> None:
            if e.messages and e.messages[-1].get("role") == "user":
                e.messages[-1]["content"].append({"text": note})

        return Transform(apply=add_note, reason=note) if event.messages else Proceed()

    def before_model_call(self, event, **kwargs):
        self.model_calls += 1
        if self.max_model_calls is not None and self.model_calls > self.max_model_calls:
            return Deny(reason=f"{DENY_TAG} model-call limit ({self.max_model_calls}) reached for this wake")
        return Proceed()
