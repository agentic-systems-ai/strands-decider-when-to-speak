"""Tests for the interjection policy pattern. No GPU, no AWS: FakeDeciderClient only."""

from __future__ import annotations

from decider_client import FakeDeciderClient

from interjection_policy import (
    Action,
    InterjectionGate,
    RollingWindow,
    Thresholds,
    TieredPolicy,
    make_interjection_questions,
    meeting_questions,
)
from interjection_policy.window import LATEST_MARK, approx_tokens

TH = {"action_item": Thresholds(0.8, 0.4), "decision_made": Thresholds(0.8, 0.4)}


def test_tiers():
    p = TieredPolicy(TH, dedupe=None)
    assert p.decide({"action_item": 0.9}, 0).action is Action.SPEAK
    assert p.decide({"action_item": 0.5}, 1).action is Action.NOTE
    assert p.decide({"action_item": 0.1}, 2).action is Action.SILENT


def test_highest_tier_then_confidence_wins():
    p = TieredPolicy(TH, dedupe=None)
    r = p.decide({"action_item": 0.95, "decision_made": 0.85}, 0)
    assert (r.action, r.category) == (Action.SPEAK, "action_item")
    r = p.decide({"action_item": 0.6, "decision_made": 0.82}, 0)
    assert r.category == "decision_made"


def test_cooldown_downgrades_to_note():
    p = TieredPolicy(TH, cooldown_s=60, dedupe=None)
    assert p.decide({"action_item": 0.9}, 100).action is Action.SPEAK
    p.record_spoken(100)
    r = p.decide({"action_item": 0.9}, 130)
    assert r.action is Action.NOTE and any("cooldown" in x for x in r.reasons)
    assert p.decide({"action_item": 0.9}, 161).action is Action.SPEAK


def test_dedupe_suppresses():
    p = TieredPolicy(TH)
    r = p.decide({"action_item": 0.95, "already_flagged": 0.8}, 0)
    assert r.action is Action.SILENT


def test_streak():
    p = TieredPolicy({"off_agenda": Thresholds(0.7, 0.5, min_streak=3)}, dedupe=None)
    assert p.decide({"off_agenda": 0.9}, 0).action is Action.SILENT
    assert p.decide({"off_agenda": 0.9}, 1).action is Action.SILENT
    assert p.decide({"off_agenda": 0.9}, 2).action is Action.SPEAK
    # streak resets after firing, and a quiet tick resets it too
    assert p.decide({"off_agenda": 0.9}, 3).action is Action.SILENT
    p.decide({"off_agenda": 0.1}, 4)
    assert p.decide({"off_agenda": 0.9}, 5).action is Action.SILENT


def test_window_latest_marker_and_budget():
    w = RollingWindow(max_tokens=120, max_lines=50)
    for i in range(40):
        w.add("Dana", f"line number {i} with a few extra words to pad it out")
    s = w.render({"AGENDA ITEM (current)": "Launch date"})
    assert s.startswith("AGENDA ITEM (current): Launch date")
    assert s.splitlines()[-1].startswith(LATEST_MARK + "[Dana] line number 39")
    assert approx_tokens(s) <= 120 + 10  # per-line rounding slack
    assert "line number 0 " not in s


def test_window_long_monologue_keeps_tail():
    w = RollingWindow(max_tokens=60)
    w.add("Raj", "blah " * 500 + "THE END")
    s = w.render()
    assert s.rstrip().endswith("THE END") and LATEST_MARK in s


def test_questions_builder():
    qs = make_interjection_questions({"bug_report": "a bug report"})
    assert qs[0].qtype == "noul" and set(qs[0].options) == {"true", "false"}
    keys = [q.key for q in meeting_questions([("launch", "pick a date")], pending_question=True)]
    assert keys == ["action_item", "decision_made", "factual_claim", "open_question",
                    "answered_prior", "agenda_item", "already_flagged"]


def test_gate_with_fake_decider():
    fake = FakeDeciderClient(lambda state, q: 0.93 if q.key == "action_item" and "I'll" in state else None)
    gate = InterjectionGate(fake, meeting_questions([("launch", "pick a date")]),
                            TieredPolicy({"action_item": Thresholds(0.8, 0.4),
                                          "off_agenda": Thresholds(0.7, 0.5)}),
                            choice_signals={"off_agenda": ("agenda_item", "off_agenda")})
    r = gate.should_wake(">> LATEST: [Raj] I'll send the deck to legal by Thursday.", 0)
    assert r.wake and r.category == "action_item" and abs(r.confidence - 0.93) < 1e-9
    assert "action_item 0.93" in r.ticker()
    r = gate.should_wake(">> LATEST: [Raj] Someone should look at the deck.", 1)
    assert not r.wake and r.signals["off_agenda"] == 0.0


def test_category_can_opt_out_of_cooldown_and_dedupe():
    p = TieredPolicy({"chat": Thresholds(0.8, 0.5),
                      "check": Thresholds(0.8, 0.5, cooldown=False, dedupe=False)}, cooldown_s=60)
    p.record_spoken(0.0)
    assert p.decide({"chat": 0.9}, 10.0).action is Action.NOTE
    assert p.decide({"check": 0.9}, 10.0).action is Action.SPEAK
    assert p.decide({"chat": 0.9, "already_flagged": 0.9}, 100.0).action is Action.SILENT
    assert p.decide({"check": 0.9, "already_flagged": 0.9}, 100.0).action is Action.SPEAK
