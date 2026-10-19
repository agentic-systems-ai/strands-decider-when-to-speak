"""MeetingAgent with FakeDeciderClient + a scripted Strands model that calls tools."""

from __future__ import annotations

import json
from typing import Any

from decider_client import FakeDeciderClient
from strands.models.model import Model

from when_to_speak.agent import MeetingAgent
from when_to_speak.schema import AgendaItem, Fact, MeetingPack, Utterance

PACK = MeetingPack(title="Go/no-go", org="Aurora",
                   agenda=[AgendaItem(id="launch_date", title="Launch date", goal="pick", timebox_min=10),
                           AgendaItem(id="crash", title="Crash", goal="review", timebox_min=10)],
                   facts=[Fact(id="F7", key="crash_free", statement="Crash-free sessions = 99.2%", value="99.2%")])


class ToolScriptModel(Model):
    """First call: emit the scripted tool calls. Second call: finish."""

    def __init__(self, script):
        self.script = script  # fn(prompt_text) -> list[(tool_name, input)]
        self.calls = 0

    def update_config(self, **kw: Any) -> None: ...

    def get_config(self) -> Any:
        return {}

    def structured_output(self, *a, **kw):  # pragma: no cover
        raise NotImplementedError

    async def stream(self, messages, tool_specs=None, system_prompt=None, **kw):
        self.calls += 1
        yield {"messageStart": {"role": "assistant"}}
        last = messages[-1]
        text = "\n".join(b.get("text", "") for b in last["content"])
        if any("toolResult" in b for b in last["content"]) or not self.script(text):
            yield {"contentBlockStart": {"start": {}}}
            yield {"contentBlockDelta": {"delta": {"text": "done"}}}
            yield {"contentBlockStop": {}}
            yield {"messageStop": {"stopReason": "end_turn"}}
            return
        for i, (name, inp) in enumerate(self.script(text)):
            yield {"contentBlockStart": {"start": {"toolUse": {"toolUseId": f"t{self.calls}-{i}", "name": name}}}}
            yield {"contentBlockDelta": {"delta": {"toolUse": {"input": json.dumps(inp)}}}}
            yield {"contentBlockStop": {}}
        yield {"messageStop": {"stopReason": "tool_use"}}


def decider_script(state: str, q) -> Any:
    latest = state.splitlines()[-1]
    if q.key == "factual_claim" and "97" in latest:
        return 0.93
    if q.key == "open_question" and "?" in latest:
        return 0.9
    if q.key == "answered_prior":
        return 0.05
    if q.key == "agenda_item":
        return "launch_date"
    return 0.02


def model_script(prompt: str):
    if "'factual_claim'" in prompt:
        return [("check_fact", {"claim": "97%", "fact_id": "F7", "verdict": "contradicted", "sheet_value": "99.2%"}),
                ("compose_interjection", {"text": "Quick check: the pre-read says 99.2%, not 97%."})]
    if "'unanswered_nudge'" in prompt:
        return [("compose_interjection", {"text": "Dana's question about screenshots is still open. Park it or assign it?"})]
    return []


def _agent():
    model = ToolScriptModel(model_script)
    return MeetingAgent(PACK, FakeDeciderClient(decider_script), model=model, cooldown_s=60), model


def _u(spk, text, t, i):
    return Utterance(speaker=spk, text=text, t_start=t - 2, t_end=t, turn_index=i)


def test_quiet_ticks_never_wake_llm():
    agent, model = _agent()
    for i, line in enumerate(["morning all", "let's get going", "sounds good"]):
        r = agent.on_utterance(_u("Raj", line, 5 + i * 5, i))
        assert r.action == "silent" and not r.woke_llm
    assert model.calls == 0


def test_contradicted_claim_is_spoken_then_cooldown():
    agent, model = _agent()
    r = agent.on_utterance(_u("Raj", "crash-free is like 97% right now", 10, 0))
    assert r.woke_llm and r.category == "factual_claim"
    assert r.spoken == "Quick check: the pre-read says 99.2%, not 97%."
    kinds = [c.kind for c in r.cards]
    assert "factual_claim" in kinds
    fc = next(c for c in r.cards if c.kind == "factual_claim")
    assert fc.data["verdict"] == "contradicted" and abs(fc.confidence - 0.93) < 1e-9
    # 20 s later the same thing: a figure claim still wakes the LLM to check it, but the
    # same fact is not corrected out loud twice.
    r2 = agent.on_utterance(_u("Raj", "yeah 97 is what I saw", 30, 1))
    assert r2.woke_llm and r2.spoken is None
    assert any(c.kind == "note" and c.data.get("reason") == "already corrected" for c in r2.cards)


def test_figure_check_covers_dates():
    from when_to_speak.agent import FIGURE
    for s in ["launch is mid-February", "we said Thursday", "ship it in May", "about 97%", "fifteen thousand"]:
        assert FIGURE.search(s), s
    for s in ["we may need more time", "sounds good to me", "let's move on"]:
        assert not FIGURE.search(s), s


def test_pending_question_nudges_after_two_ticks():
    agent, _ = _agent()
    r = agent.on_utterance(_u("Dana", "Who owns the app store screenshots?", 10, 0))
    assert agent.state.pending is not None and any(c.kind == "open_question" for c in r.cards)
    r = agent.on_utterance(_u("Raj", "anyway, the date", 15, 1))
    assert r.spoken is None
    r = agent.on_utterance(_u("Mei", "June works for me", 20, 2))
    assert r.category == "unanswered_nudge" and r.spoken and "still open" in r.spoken
    assert agent.state.pending is None


def test_figure_claim_only_wakes_when_latest_line_has_a_figure():
    # Decider still scores factual_claim high (the 97% is in the window), but the latest line
    # has no figure, so the LLM is not woken again.
    def sticky(state, q):
        return 0.93 if q.key == "factual_claim" else decider_script(state, q)

    model = ToolScriptModel(model_script)
    agent = MeetingAgent(PACK, FakeDeciderClient(sticky), model=model, cooldown_s=0)
    r = agent.on_utterance(_u("Raj", "crash-free is like 97% right now", 10, 0))
    assert r.woke_llm
    r = agent.on_utterance(_u("Mei", "ok, moving on to the launch date", 20, 1))
    assert not r.woke_llm and r.signals["factual_claim"] == 0.0


def test_supported_claim_and_decisions_never_speak():
    def script(prompt):
        if "'factual_claim'" in prompt:
            return [("check_fact", {"claim": "99.2%", "fact_id": "F7", "verdict": "supported"}),
                    ("compose_interjection", {"text": "That matches the pre-read."})]
        if "'decision_made'" in prompt:
            return [("record_decision", {"decision": "Launch June 3"}),
                    ("compose_interjection", {"text": "Decided: June 3."})]
        return []

    def decider(state, q):
        latest = state.splitlines()[-1]
        if q.key == "factual_claim" and "99.2" in latest:
            return 0.93
        if q.key == "decision_made" and "decided" in latest:
            return 0.95
        return decider_script(state, q)

    agent = MeetingAgent(PACK, FakeDeciderClient(decider), model=ToolScriptModel(script), cooldown_s=0)
    r = agent.on_utterance(_u("Raj", "crash-free is 99.2% this week", 10, 0))
    assert r.woke_llm and r.spoken is None
    r = agent.on_utterance(_u("Mei", "ok, decided, we launch June 3", 20, 1))
    assert r.woke_llm and r.category == "decision_made" and r.spoken is None
    assert any(c.kind == "decision_made" for c in r.cards)


def test_recap_accepts_structured_action_items():
    from when_to_speak.agent import Recap

    r = Recap.model_validate({"decisions": ["Launch June 3"], "open_questions": [], "corrected_facts": [],
                              "summary": "s", "action_items": [{"owner": "Raj", "task": "send deck", "due": "Fri"}]})
    assert r.action_items == ["Raj: send deck (due Fri)"]


def test_correction_outranks_cooldown_after_nudge():
    agent, _ = _agent()
    agent.on_utterance(_u("Dana", "Who owns the app store screenshots?", 10, 0))
    agent.on_utterance(_u("Raj", "anyway, the date", 15, 1))
    r = agent.on_utterance(_u("Mei", "June works for me", 20, 2))
    assert r.spoken  # the nudge starts the cooldown
    r = agent.on_utterance(_u("Raj", "crash-free is like 97% right now", 30, 3))
    assert r.spoken == "Quick check: the pre-read says 99.2%, not 97%."


def test_ungated_agent_wakes_every_line_and_names_its_category():
    def script(prompt: str):
        if "97%" in prompt.split("MEETING STATE")[0]:
            return [("check_fact", {"claim": "97%", "fact_id": "F7", "verdict": "contradicted", "sheet_value": "99.2%"}),
                    ("compose_interjection", {"text": "Quick check: the pre-read says 99.2%, not 97%.",
                                              "category": "factual_claim"})]
        return []
    model = ToolScriptModel(script)
    agent = MeetingAgent(PACK, None, model=model, cooldown_s=60, gated=False)
    r = agent.on_utterance(_u("Raj", "morning all", 5, 0))
    assert r.woke_llm and r.spoken is None and model.calls == 1
    r = agent.on_utterance(_u("Raj", "crash-free is like 97% right now", 10, 1))
    assert r.spoken == "Quick check: the pre-read says 99.2%, not 97%."
    assert any(c.kind == "factual_claim" and c.spoken for c in r.cards)


def test_only_a_question_mark_starts_a_pending_question():
    def script(state, q):
        return 0.9 if q.key == "open_question" else decider_script(state, q)
    agent = MeetingAgent(PACK, FakeDeciderClient(script), model=ToolScriptModel(model_script), cooldown_s=60)
    agent.on_utterance(_u("Mom", "can we please keep it to the list this time", 5, 0))
    assert agent.state.pending is None
    agent.on_utterance(_u("Dana", "Who owns the app store screenshots?", 10, 1))
    assert agent.state.pending is not None


def test_off_topic_streak_wakes_a_nudge():
    def script(state, q):
        return 0.9 if q.key == "off_agenda" else decider_script(state, q)
    def nudge(prompt):
        return [("compose_interjection", {"text": "Shall we get back to the launch date?"})] if "'off_agenda'" in prompt else []
    agent = MeetingAgent(PACK, FakeDeciderClient(script), model=ToolScriptModel(nudge), cooldown_s=60)
    spoken = [agent.on_utterance(_u("Raj", f"did you see the game {i}", 5 + 5 * i, i)).spoken for i in range(3)]
    assert spoken[:2] == [None, None] and spoken[2] == "Shall we get back to the launch date?"


def test_spoken_line_drops_name_brackets():
    def script(prompt: str):
        if "'unanswered_nudge'" in prompt:
            return [("compose_interjection", {"text": "[Dana], about <screenshots>: park it or assign it?"})]
        return []
    agent = MeetingAgent(PACK, FakeDeciderClient(decider_script), model=ToolScriptModel(script), cooldown_s=60)
    agent.on_utterance(_u("Dana", "Who owns the app store screenshots?", 10, 0))
    agent.on_utterance(_u("Raj", "anyway, the date", 15, 1))
    r = agent.on_utterance(_u("Mei", "June works for me", 20, 2))
    assert r.spoken == "Dana, about screenshots: park it or assign it?"
