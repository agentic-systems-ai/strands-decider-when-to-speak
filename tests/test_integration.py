"""Mode-A replay of a simulated meeting through the agent, scored at event level.

The fake decider "sees" the planted markers the fake simulator writes into each line,
so this checks the plumbing (replay -> gate -> agent tools -> cards -> scoring), not
model quality.
"""

from __future__ import annotations

import asyncio

from decider_client import FakeDeciderClient

from test_agent import ToolScriptModel
from test_simulator import _run
from when_to_speak.agent import MeetingAgent
from when_to_speak.replay import text_replay
from when_to_speak.scoring import score_meeting


def decider_script(state, q):
    latest = state.splitlines()[-1]
    # factual_claim / open_question fire on positives and hard negatives alike (both state a
    # figure / ask a question); Bedrock's check and the pending logic tell them apart.
    marks = {"action_item": "<<action_item:pos>>", "decision_made": "<<decision_made:pos>>",
             "factual_claim": "<<factual_claim:", "open_question": "<<unanswered_question:"}
    if q.key in marks:
        return 0.95 if marks[q.key] in latest else 0.03
    if q.key == "answered_prior":
        return 0.9 if "<<answer>>" in latest else 0.05
    if q.key == "agenda_item":
        return "off_agenda" if "<<off_topic_drift" in latest else None
    return 0.02


def model_script(prompt):
    if "'action_item'" in prompt:
        return [("extract_action_item", {"owner": "X", "task": "do it", "due": "Thu"})]
    if "'decision_made'" in prompt:
        return [("record_decision", {"decision": "decided"})]
    if "'factual_claim'" in prompt:
        latest = prompt.split("Latest line:")[1].splitlines()[0]
        verdict = "contradicted" if ":pos>>" in latest else "supported"
        calls = [("check_fact", {"claim": "n", "fact_id": "F1", "verdict": verdict, "sheet_value": "99.2%"})]
        if verdict == "contradicted":
            calls.append(("compose_interjection", {"text": "Quick check: the pre-read says 99.2%."}))
        return calls
    if "'unanswered_nudge'" in prompt or "'off_agenda'" in prompt:
        return [("compose_interjection", {"text": "Let's park that and come back to the agenda."})]
    return []


def test_replay_agent_score():
    m = _run()
    agent = MeetingAgent(m.cast.pack, FakeDeciderClient(decider_script), model=ToolScriptModel(model_script),
                         cooldown_s=60)

    async def go():
        async for u in text_replay(m, speed=0):
            agent.on_utterance(u)

    asyncio.run(go())
    s = score_meeting(m, agent.ticks)
    assert s.ticks == len(m.turns)
    # every planted action item / decision is caught (no cooldown on silent cards)
    for cat in ("action_item", "decision_made"):
        assert s.per_category[cat].fn == 0, (cat, s.misses)
        assert s.per_category[cat].fp_on_hard_neg == 0
    # spoken lines respect the 60 s cooldown
    spoken_t = [t.t for t in agent.ticks if t.spoken]
    assert all(b - a >= 60 for a, b in zip(spoken_t, spoken_t[1:]))
    assert s.unjustified_spoken == 0, s.false_alarms
    assert s.llm_skip_rate > 0.5
