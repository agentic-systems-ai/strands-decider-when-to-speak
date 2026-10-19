"""The meeting agent: Decider decides *whether* to wake, Bedrock decides *what* to say.

Every final utterance is a tick. The agent is a Strands Agent (Bedrock) with tools; the
interjection policy runs as a `before_invocation` intervention, so a quiet tick is denied
before any model call. When it wakes, the agent knows which category fired and how
confident Decider was, and uses its tools:

    extract_action_item  -> action card; speak only to ask for a missing due date
    record_decision      -> decision card (rarely spoken)
    check_fact           -> supported / contradicted / not_in_sheet; speak only if contradicted
    compose_interjection -> the spoken line (<= 20 words), subject to the cooldown
    write_recap          -> end of meeting (a separate structured call)

State that the policy cannot see on its own (the pending question) is handled here.
"""

from __future__ import annotations

import re
import time
from collections.abc import Callable
from typing import Any, Literal

from pydantic import BaseModel, field_validator
from strands import Agent, tool

from interjection_policy import (
    Action,
    GateResult,
    InterjectionGate,
    InterjectionIntervention,
    Thresholds,
    TieredPolicy,
)
from interjection_policy.strands_wiring import STATE_KEY

from . import providers
from .schema import MeetingPack, Utterance
from .state import MeetingState, Pending

# Categories whose wake records a card or checks a figure skip the wake cooldown: the
# compose_interjection tool still enforces it on anything spoken.
DEFAULT_THRESHOLDS: dict[str, Thresholds] = {
    "action_item": Thresholds(speak=0.85, note=0.5, cooldown=False),
    "decision_made": Thresholds(speak=0.85, note=0.5, cooldown=False),
    # Only the LLM can compare a figure with the fact sheet, so any figure claim on the latest
    # line wakes it (see _derive); it speaks only on a contradiction. The latest-line check
    # replaces already_flagged as the dedupe.
    "factual_claim": Thresholds(speak=0.50, note=0.5, cooldown=False, dedupe=False),
    "open_question": Thresholds(speak=1.01, note=0.6),     # never wakes; starts a pending question
    "unanswered_nudge": Thresholds(speak=0.80, note=0.80),  # pending question still open after 2 ticks
    "off_agenda": Thresholds(speak=0.70, note=0.5, min_streak=3),
}
_NUMBER_WORDS = ("one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|"
                 "sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|"
                 "hundred|thousand|million|billion|half|dozen|percent|grand")
_DATE_WORDS = ("january|february|march|april|june|july|august|september|october|november|december|"
               "jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec|"
               "monday|tuesday|wednesday|thursday|friday|saturday|sunday")
# "May" only capitalised: lowercase it is usually the verb.
FIGURE = re.compile(rf"\d|\b({_NUMBER_WORDS}|{_DATE_WORDS})\b|(?-i:\bMay\b)", re.I)
NUDGE_AFTER_TICKS = 2
# Decider's answered_prior is under-confident: on dev, p >= 0.3 is the best cut (F1 0.83 vs 0.54 at 0.5).
ANSWERED_AT = 0.3
PENDING_GIVE_UP_TICKS = 5
MAX_SPOKEN_WORDS = 20
LLM_ATTEMPTS = 3

SYSTEM_PROMPT = """You are an assistant facilitator sitting in on a meeting. You are almost always silent.
A separate decision model wakes you only when something in the latest line may need you, and tells you
which category it flagged and how confident it is. Act through your tools, then stop.

By category:
- action_item: call extract_action_item(owner, task, due). If no due date or time was given, also call
  compose_interjection to ask the owner, in the form "<owner>, by when?". Otherwise stay silent.
- decision_made: call record_decision with a one-line record. Do not speak.
- factual_claim: compare the claim with the FACT SHEET VALUES and call check_fact. Only if the verdict is
  "contradicted", call compose_interjection with a short, friendly correction citing the pre-read, in
  the form "Quick check: the pre-read says <sheet value>, not <spoken value>." Never speak to confirm a
  figure that matches.
- unanswered_nudge: call compose_interjection to name the open question from the transcript (who asked,
  about what) and ask to park or assign it.
- off_agenda: call compose_interjection with a gentle nudge back to the current agenda item.

The <...> parts are placeholders: fill them from this meeting's transcript, never copy them literally.
If the flag looks wrong on reading the transcript, do nothing. Spoken lines: at most 20 words, warm,
plain, no preamble. Never speak more than once per wake. Your final text reply is ignored."""

# Baseline without the Decider: the LLM sees every line and judges the categories itself.
UNGATED_SYSTEM_PROMPT = SYSTEM_PROMPT.replace(
    """A separate decision model wakes you only when something in the latest line may need you, and tells you
which category it flagged and how confident it is. Act through your tools, then stop.""",
    """You see every line of the meeting. Most lines need nothing from you: then do nothing and reply "ok".
If the latest line falls into one of the categories below, act through your tools, then stop. When you
call compose_interjection, pass the category it is for.""").replace(
    "If the flag looks wrong on reading the transcript, do nothing.",
    "If no category clearly applies, do nothing.")


class AlwaysWake:
    """Stands in for InterjectionGate when there is no Decider: every tick wakes the LLM."""

    def should_wake(self, state: str, now: float) -> GateResult:
        return GateResult(action=Action.SPEAK, category=None, confidence=1.0, reasons=["ungated"],
                          decisions={}, signals={}, latency_ms=0.0, state=state)


# Categories whose wake may end in a spoken line; anything else becomes a silent note.
MAY_SPEAK = {"action_item", "factual_claim", "unanswered_nudge", "off_agenda"}


class Card(BaseModel):
    kind: Literal["action_item", "decision_made", "factual_claim", "open_question", "unanswered_nudge",
                  "off_agenda", "note"]
    t: float
    category: str
    confidence: float
    text: str
    spoken: bool = False
    data: dict[str, Any] = {}


class Recap(BaseModel):
    decisions: list[str]
    action_items: list[str]
    open_questions: list[str]
    corrected_facts: list[str]
    summary: str

    @field_validator("decisions", "action_items", "open_questions", "corrected_facts", mode="before")
    @classmethod
    def _flatten(cls, v: Any) -> Any:
        """Small models return {"owner": ..., "task": ..., "due": ...} where a line is asked for."""
        if not isinstance(v, list):
            return v
        out = []
        for item in v:
            if isinstance(item, dict):
                if "task" in item:
                    item = f"{item.get('owner', '?')}: {item['task']}" + (f" (due {item['due']})" if item.get("due") else "")
                else:
                    item = "; ".join(str(x) for x in item.values())
            out.append(item)
        return out


class TickResult(BaseModel):
    t: float
    speaker: str
    text: str
    turn_index: int | None
    action: str
    category: str | None
    confidence: float
    signals: dict[str, float]
    reasons: list[str]
    decider_ms: float
    woke_llm: bool
    llm_ms: float = 0.0
    cards: list[Card] = []
    spoken: str | None = None


def default_model(model_id: str | None = None):
    """The agent's model: ollama (default, for prototyping) or Bedrock, per LLM_PROVIDER."""
    return providers.strands_model("main", model=model_id, max_tokens=600)


class MeetingAgent:
    def __init__(self, pack: MeetingPack, decider: Any, *, model: Any = None,
                 thresholds: dict[str, Thresholds] | None = None, cooldown_s: float = 60.0,
                 emit: Callable[[str, dict], None] | None = None, gated: bool = True):
        self.pack = pack
        self.gated = gated
        self.state = MeetingState(pack)
        self.policy = TieredPolicy(thresholds or DEFAULT_THRESHOLDS, cooldown_s=cooldown_s)
        self.gate = InterjectionGate(decider, self.state.questions, self.policy,
                                     derive=self._derive) if gated else AlwaysWake()
        self.hook = InterjectionIntervention(self.gate, on_result=self._on_gate,
                                             clock=lambda: self.state.now)
        self.emit = emit or (lambda kind, payload: None)
        self.cards: list[Card] = []
        self.ticks: list[TickResult] = []
        self.llm_usage = {"wakes": 0, "input_tokens": 0, "output_tokens": 0}
        self._model = model
        self._tick_cards: list[Card] = []
        self._tick_spoken: str | None = None
        self._tick_contradicted: str | None = None  # fact id (or sheet value) of this tick's contradicted claim
        self._corrected_aloud: set[str] = set()
        self._last: GateResult | None = None
        self.agent = Agent(model=model or default_model(), tools=self._tools(),
                           system_prompt=SYSTEM_PROMPT if gated else UNGATED_SYSTEM_PROMPT,
                           interventions=[self.hook], callback_handler=None)

    # ------------------------------------------------------------- tools

    def _card(self, kind: str, text: str, spoken: bool = False, **data: Any) -> Card:
        res = self._last
        c = Card(kind=kind, t=self.state.now, category=res.category if res and res.category else kind,
                 confidence=res.confidence if res else 0.0, text=text, spoken=spoken, data=data)
        self._tick_cards.append(c)
        self.cards.append(c)
        self.emit("card", c.model_dump())
        return c

    def _tools(self) -> list:
        agent = self

        @tool
        def extract_action_item(owner: str, task: str, due: str = "") -> str:
            """Record an action item someone committed to.

            Args:
                owner: The person who committed.
                task: What they will do, as a short imperative phrase.
                due: The deadline if one was said, else empty.
            """
            agent._card("action_item", f"{owner}: {task}" + (f" (due {due})" if due else ""),
                        owner=owner, task=task, due=due)
            agent.state.flag(f"ACTION {owner}: {task}")
            return "recorded" + ("" if due else "; no due date was given")

        @tool
        def record_decision(decision: str) -> str:
            """Record a decision the group made, as one line."""
            agent._card("decision_made", decision)
            agent.state.flag(f"DECISION {decision}")
            return "recorded"

        @tool
        def check_fact(claim: str, fact_id: str, verdict: Literal["supported", "contradicted", "not_in_sheet"],
                       sheet_value: str = "") -> str:
            """Record your check of a spoken claim against the fact sheet.

            Args:
                claim: The figure as spoken.
                fact_id: The matching fact id (e.g. F7), or empty.
                verdict: supported, contradicted or not_in_sheet.
                sheet_value: The fact sheet's value, if any.
            """
            agent._card("factual_claim", f"{claim} -> {verdict}" + (f" (sheet: {sheet_value})" if sheet_value else ""),
                        claim=claim, fact_id=fact_id, verdict=verdict, sheet_value=sheet_value)
            if verdict == "contradicted":
                agent._tick_contradicted = fact_id or sheet_value or claim
                agent.state.flag(f"CORRECTED {claim} (sheet {sheet_value})")
            return verdict

        def speak(text: str, cat: str | None) -> str:
            # Models sometimes keep the prompt's "<owner>" placeholder brackets, or the transcript's
            # "[Raj]" speaker tag, around a name.
            words = re.sub(r"[<>\[\]]", "", text).split()
            line = " ".join(words[:MAX_SPOKEN_WORDS])
            if cat not in MAY_SPEAK or (cat == "factual_claim" and not agent._tick_contradicted):
                agent._card("note", line, reason="not a speaking category")
                return "not spoken: this flag does not call for speaking; kept as a silent note"
            # A correction of a wrong figure outranks the cooldown (a nudge may have just used it
            # up), but each fact is corrected out loud only once.
            fact = agent._tick_contradicted if cat == "factual_claim" else None
            if fact and fact in agent._corrected_aloud:
                agent._card("note", line, reason="already corrected")
                return "not spoken: this figure was already corrected; kept as a silent note"
            if agent._tick_spoken or (not fact and agent.policy.in_cooldown(agent.state.now)):
                agent._card("note", line, reason="cooldown")
                return "not spoken (cooldown); kept as a silent note"
            if fact:
                agent._corrected_aloud.add(fact)
            agent.policy.record_spoken(agent.state.now)
            agent._tick_spoken = line
            agent._card(cat or "note", line, spoken=True)
            agent.emit("speak", {"t": agent.state.now, "text": line})
            return "spoken"

        if agent.gated:
            @tool
            def compose_interjection(text: str) -> str:
                """Say something out loud to the meeting. At most 20 words."""
                return speak(text, agent._last.category if agent._last else None)
        else:
            @tool
            def compose_interjection(text: str, category: Literal["action_item", "factual_claim",  # type: ignore[no-redef]
                                                                 "unanswered_nudge", "off_agenda"]) -> str:
                """Say something out loud to the meeting. At most 20 words.

                Args:
                    text: The line to say.
                    category: The category this line is for.
                """
                return speak(text, category)

        return [extract_action_item, record_decision, check_fact, compose_interjection]

    # ------------------------------------------------------------- gate glue

    def _on_gate(self, res: GateResult) -> None:
        self._last = res  # set before any tool runs, so cards carry this tick's category
        self.emit("gate", {"t": self.state.now, "action": res.action.value, "category": res.category,
                           "confidence": res.confidence, "wake": res.wake, "reasons": res.reasons,
                           "signals": {k: round(v, 4) for k, v in res.signals.items()},
                           "decider_ms": res.latency_ms})

    def _derive(self, decisions, signals) -> dict[str, float]:
        out: dict[str, float] = {}
        # Decider keeps scoring a figure high while it is anywhere in the window; only a figure
        # on the latest line is new.
        if "factual_claim" in signals and not FIGURE.search(self.state.latest):
            out["factual_claim"] = 0.0
        p = self.state.pending
        if p is None or "answered_prior" not in decisions:
            out["unanswered_nudge"] = 0.0
        else:
            p_answered = decisions["answered_prior"].p_true
            out["unanswered_nudge"] = (1.0 - p_answered) if p.ticks >= NUDGE_AFTER_TICKS else 0.0
        return out

    def _prompt(self, u: Utterance) -> str:
        facts = "\n".join(f"- {f.id} [{f.key}]: {f.statement}" for f in self.pack.facts)
        return (f"t={u.t_end:.0f}s. Latest line: [{u.speaker}] {u.text}\n\n"
                f"MEETING STATE:\n{self.state.render()}\n\nFACT SHEET VALUES:\n{facts}")

    # ------------------------------------------------------------- the tick

    def on_utterance(self, u: Utterance) -> TickResult:
        if not u.is_final:
            raise ValueError("tick on final utterances only")
        self.state.add(u.speaker, u.text, u.t_end)
        if self.state.pending:
            self.state.pending.ticks += 1
        self._tick_cards, self._tick_spoken, self._tick_contradicted = [], None, None

        state = self.state.render()
        self.agent.messages.clear()  # stateless per wake: context comes in the prompt
        t0 = time.perf_counter()
        for attempt in range(LLM_ATTEMPTS):
            try:
                result = self.agent(self._prompt(u), invocation_state={STATE_KEY: state})
                break
            except Exception:  # a timed-out or throttled model call; the tick is retried whole
                if attempt == LLM_ATTEMPTS - 1:
                    raise
                self.agent.messages.clear()
                self._tick_cards, self._tick_spoken, self._tick_contradicted = [], None, None
        res = self.hook.last_result
        llm_ms = 0.0
        if res.wake:
            llm_ms = (time.perf_counter() - t0) * 1000 - res.latency_ms
            # accumulated_usage is a running total over the agent's life, not this invocation.
            usage = result.metrics.accumulated_usage
            self.llm_usage["wakes"] += 1
            self.llm_usage["input_tokens"] = usage.get("inputTokens", 0)
            self.llm_usage["output_tokens"] = usage.get("outputTokens", 0)

        self._after_tick(u, res)
        tr = TickResult(t=u.t_end, speaker=u.speaker, text=u.text, turn_index=u.turn_index,
                        action=res.action.value, category=res.category, confidence=res.confidence,
                        signals={k: round(v, 4) for k, v in res.signals.items()}, reasons=res.reasons,
                        decider_ms=res.latency_ms, woke_llm=res.wake, llm_ms=llm_ms,
                        cards=list(self._tick_cards), spoken=self._tick_spoken)
        self.ticks.append(tr)
        self.emit("tick", tr.model_dump(exclude={"cards"}))
        return tr

    def _after_tick(self, u: Utterance, res: GateResult) -> None:
        sig = res.signals
        th = self.policy.thresholds
        # Pending-question bookkeeping.
        if self.state.pending:
            if res.wake and res.category == "unanswered_nudge":
                self.state.pending = None
            elif "answered_prior" in res.decisions and res.decisions["answered_prior"].p_true >= ANSWERED_AT:
                self.state.pending = None
            elif self.state.pending.ticks >= PENDING_GIVE_UP_TICKS:
                self.state.pending = None
        # Only a line with a question mark starts a pending question (dev: precision 0.36 -> 0.93).
        if (sig.get("open_question", 0.0) >= th["open_question"].note and "?" in u.text
                and self.state.pending is None):
            self.state.pending = Pending(u.speaker, u.text, u.turn_index, u.t_end)
            self._card("open_question", f"[{u.speaker}] {u.text}", p=sig["open_question"])
        # Silent margin note for a category that reached the NOTE tier without waking the LLM.
        if res.action is Action.NOTE and res.category not in ("open_question",):
            self._card("note", f"[{u.speaker}] {u.text}", tier="note")

    # ------------------------------------------------------------- end of meeting

    def recap(self, llm: Any = None) -> Recap:
        """Bedrock writes the recap from the collected cards (not the transcript)."""
        from .llm import LLM

        llm = llm or LLM()
        lines = "\n".join(f"- [{c.kind}{' SPOKEN' if c.spoken else ''}] {c.text}" for c in self.cards)
        user = (f"Meeting: {self.pack.title}\nCards collected during the meeting:\n{lines or '(none)'}\n\n"
                "Write the recap: decisions, action items (owner: task, due), open questions, corrected "
                "facts, and a 2-sentence summary. Use only what the cards say.")
        return llm.structured("You write crisp meeting recaps.", user, Recap, name="submit_recap",
                              max_tokens=1500, temperature=0.2)
