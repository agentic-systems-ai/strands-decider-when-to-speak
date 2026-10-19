"""Event-level scoring of an agent run against a meeting's gold events (spec §9).

A gold positive counts as caught if the agent surfaced the right category within a
tolerance window after its target turn:

    action_item, decision_made   a card (spoken or silent) within [t, t+2]
    factual_claim (contradicted) a spoken correction within [t, t+2]
    unanswered_question          a spoken nudge within [t, t+2+NUDGE_AFTER_TICKS+1]
    off_topic_drift              a spoken nudge within [t, t+span+2]

Annoyance = spoken interjections that no gold positive justifies, per meeting-hour.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence

from pydantic import BaseModel

from .agent import NUDGE_AFTER_TICKS, TickResult
from .schema import CATEGORIES, GoldEvent, Meeting

TOL = 2
# agent card/category -> gold category
AGENT_TO_GOLD = {"action_item": "action_item", "decision_made": "decision_made",
                 "factual_claim": "factual_claim", "unanswered_nudge": "unanswered_question",
                 "off_agenda": "off_topic_drift"}
SPOKEN_ONLY = {"factual_claim", "unanswered_question", "off_topic_drift"}


def window(g: GoldEvent) -> range:
    if g.category == "unanswered_question":
        return range(g.turn_index, g.turn_index + TOL + NUDGE_AFTER_TICKS + 2)
    if g.category == "off_topic_drift":
        return range(g.turn_index, g.turn_index + max(1, g.span_turns) + TOL + 1)
    return range(g.turn_index, g.turn_index + TOL + 1)


class Detection(BaseModel):
    tick: int
    category: str          # gold category space
    spoken: bool
    confidence: float
    text: str


class CategoryScore(BaseModel):
    tp: int = 0
    fn: int = 0
    fp: int = 0
    fp_on_hard_neg: int = 0

    @property
    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if self.tp + self.fp else 1.0

    @property
    def recall(self) -> float:
        return self.tp / (self.tp + self.fn) if self.tp + self.fn else 1.0


class MeetingScore(BaseModel):
    meeting_id: str
    minutes: float
    ticks: int
    wakes: int
    spoken: int
    unjustified_spoken: int
    per_category: dict[str, CategoryScore]
    misses: list[str]
    false_alarms: list[str]

    @property
    def annoyance_per_hour(self) -> float:
        return self.unjustified_spoken / (self.minutes / 60) if self.minutes else 0.0

    @property
    def llm_skip_rate(self) -> float:
        return 1 - self.wakes / self.ticks if self.ticks else 1.0


def detections(ticks: Sequence[TickResult]) -> list[Detection]:
    out = []
    for i, tr in enumerate(ticks):
        tick = tr.turn_index if tr.turn_index is not None else i
        for c in tr.cards:
            cat = c.category if c.kind in ("note",) else c.kind
            gold_cat = AGENT_TO_GOLD.get(cat)
            if gold_cat is None:
                continue
            if gold_cat == "factual_claim" and not c.spoken:
                continue  # a checked-but-supported claim is not a detection of a contradiction
            out.append(Detection(tick=tick, category=gold_cat, spoken=c.spoken, confidence=c.confidence,
                                 text=c.text))
    return out


def score_meeting(m: Meeting, ticks: Sequence[TickResult]) -> MeetingScore:
    dets = detections(ticks)
    by_cat: dict[str, list[Detection]] = defaultdict(list)
    for d in dets:
        by_cat[d.category].append(d)
    scores = {c: CategoryScore() for c in CATEGORIES}
    misses, false_alarms = [], []
    hard_neg_turns = {(g.category, g.turn_index) for g in m.gold if g.polarity == "neg"}

    for cat in CATEGORIES:
        golds = m.positives(cat)
        used: set[int] = set()
        for g in golds:
            w = window(g)
            hit = next((k for k, d in enumerate(by_cat[cat]) if k not in used and d.tick in w
                        and (d.spoken or cat not in SPOKEN_ONLY)), None)
            if hit is None:
                scores[cat].fn += 1
                misses.append(f"{cat}@{g.turn_index}: {m.turns[g.turn_index].text[:80]}")
            else:
                used.add(hit)
                scores[cat].tp += 1
        for k, d in enumerate(by_cat[cat]):
            if k in used:
                continue
            # A second card for an event already caught is a duplicate, not a false alarm.
            if any(d.tick in window(g) for g in golds):
                continue
            scores[cat].fp += 1
            if any((cat, t) in hard_neg_turns for t in range(d.tick - TOL, d.tick + 1)):
                scores[cat].fp_on_hard_neg += 1
            false_alarms.append(f"{cat}@{d.tick}{' SPOKEN' if d.spoken else ''}: {d.text[:80]}")

    justified = 0
    spoken = [d for d in dets if d.spoken]
    for d in spoken:
        if any(d.tick in window(g) for g in m.positives(d.category)):
            justified += 1
    minutes = (m.timeline[-1].end_s / 60) if m.timeline else 0.0
    return MeetingScore(meeting_id=m.meeting_id, minutes=minutes, ticks=len(ticks),
                        wakes=sum(t.woke_llm for t in ticks), spoken=len(spoken),
                        unjustified_spoken=len(spoken) - justified, per_category=scores,
                        misses=misses, false_alarms=false_alarms)
