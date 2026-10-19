"""Simulator mechanics with a scripted LLM (no AWS)."""

from __future__ import annotations

import re

from when_to_speak.schema import CATEGORIES, Meeting
from when_to_speak.simulator import (
    AgendaPlanDraft,
    AuditTags,
    CastDraft,
    SimConfig,
    simulate,
)


class FakeLLM:
    """Casts 4 people, plants what it is asked to, and audits honestly from the text."""

    def __init__(self, leak_negatives: bool = False):
        self.leak = leak_negatives
        self.text_calls = 0

    def structured(self, system, user, model, **kw):
        if model is CastDraft:
            return CastDraft.model_validate({
                "personas": [{"name": n, "role": "r", "goals": "g", "hidden_agenda": "h",
                              "verbosity": v, "wpm": 150, "voice_gender": gnd}
                             for n, v, gnd in [("Dana", 4, "female"), ("Raj", 2, "male"),
                                               ("Mei", 3, "female"), ("Tom", 1, "male")]],
                "pack": {"title": "Go/no-go", "org": "Aurora", "agenda": [
                    {"id": "launch_date", "title": "Launch date", "goal": "pick", "timebox_min": 4},
                    {"id": "crash", "title": "Crash", "goal": "review", "timebox_min": 3},
                    {"id": "assets", "title": "Assets", "goal": "assign", "timebox_min": 3}],
                    "facts": [{"id": "F1", "key": "crash_free", "statement": "Crash-free = 99.2%",
                               "value": "99.2%"}]},
            })
        if model is AgendaPlanDraft:
            evs = re.findall(r"^\d+\. (\w+) / (pos|neg) / speaker: (\w+)", user, re.M)
            out = []
            for i, (cat, pol, spk) in enumerate(evs):
                e = {"category": cat, "polarity": pol, "speaker": spk, "beat_turn": 2 + 3 * i,
                     "direction": f"<<{cat}:{pol}>>", "fact_id": "F1" if cat == "factual_claim" else None}
                if cat == "unanswered_question" and pol == "neg":
                    e["followups"] = [{"after_turns": 2, "speaker": "Tom", "direction": "<<answer>>"}]
                if cat == "off_topic_drift" and pol == "pos":
                    e["followups"] = [{"after_turns": k, "speaker": "Raj", "direction": "<<off_topic_drift:cont>>"}
                                      for k in (1, 2, 3)]
                out.append(e)
            return AgendaPlanDraft.model_validate({"beats": [{"summary": "s", "n_turns": 5}] * 3, "events": out})
        if model is AuditTags:
            tags = []
            for idx, txt in re.findall(r"^(\d+): \[\w+\] (.*)$", user, re.M):
                m = re.search(r"<<(\w+):(pos|neg|cont)>>", txt)
                if not m:
                    continue
                cat, pol = m.groups()
                i = int(idx)
                leak = self.leak and pol == "neg"
                if cat in ("action_item", "decision_made") and (pol == "pos" or leak):
                    tags.append({"turn_index": i, "category": cat})
                elif cat == "factual_claim":
                    tags.append({"turn_index": i, "category": "numeric_claim", "fact_id": "F1",
                                 "contradicts_fact_sheet": pol == "pos"})
                elif cat == "unanswered_question":
                    tags.append({"turn_index": i, "category": "open_question",
                                 "answered_in_turn": None if pol == "pos" else i + 2})
                elif cat == "off_topic_drift" and pol in ("pos", "cont"):
                    tags.append({"turn_index": i, "category": "off_topic"})
            lo, hi = map(int, re.search(r"TARGET range: turns (\d+) to (\d+)", user).groups())
            tags = [t for t in tags if lo <= t["turn_index"] <= hi]
            return AuditTags.model_validate({"tags": tags})
        raise AssertionError(model)

    def text(self, system, user, **kw):
        self.text_calls += 1
        m = re.search(r"YOUR PRIVATE DIRECTION: (<<[^>]+>>)", user)
        return (m.group(1) + " so yeah") if m else "uh, sounds reasonable to me, let's keep going here then"


def _run(**kw) -> Meeting:
    return simulate(SimConfig(theme="Aurora go/no-go", duration_min=10, drama=0.6, seed=1),
                    llm=FakeLLM(**kw), progress=lambda s: None)


def test_pipeline_produces_valid_meeting():
    m = _run()
    Meeting.model_validate(m.model_dump())
    assert [t.index for t in m.turns] == list(range(len(m.turns)))
    assert len(m.timeline) == len(m.turns)
    assert {p.polly_voice for p in m.cast.personas}.__len__() == 4


def test_every_category_has_positive_and_hard_negative():
    m = _run()
    for cat in CATEGORIES:
        assert m.positives(cat), cat
        if cat != "off_topic_drift":  # drift negatives are one-liners: not auditable, but planted
            assert any(g.category == cat and g.polarity == "neg" for g in m.gold), cat


def test_planted_events_land_on_their_turns():
    m = _run()
    for g in m.gold:
        if g.source == "plan" and g.category != "off_topic_drift":
            assert f"<<{g.category}:{g.polarity}>>" in m.turns[g.turn_index].text


def test_leaked_negatives_are_dropped_after_retries():
    m = _run(leak_negatives=True)
    planted_neg = [g for g in m.gold if g.source == "plan" and g.polarity == "neg"
                   and g.category in ("action_item", "decision_made")]
    assert planted_neg == []  # the fake always leaks, so after 2 re-renders they are dropped


def test_windows_carry_labels_by_construction():
    from when_to_speak.dataset import windows
    from interjection_policy.window import LATEST_MARK

    m = _run()
    ws = list(windows(m))
    assert len(ws) == len(m.turns)
    for w in ws:
        latest = w.state.splitlines()[-1]
        assert latest.startswith(LATEST_MARK)
        if w.labels["action_item"]:
            assert "<<action_item:pos>>" in latest
        if "action_item" in w.hard_neg:
            assert w.labels["action_item"] is False
    assert any("answered_prior" in w.labels for w in ws)
    assert any(w.labels["agenda_item"] == "off_agenda" for w in ws)
