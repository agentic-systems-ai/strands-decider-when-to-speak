"""Meetings -> labelled Decider windows (one per tick = one per final utterance).

Per-window labels, derived from the gold events (labels by construction):

    action_item      a gold action_item positive is on the LATEST turn
    decision_made    a gold decision_made positive is on the LATEST turn
    factual_claim    a gold factual_claim (pos = contradicts, neg = matches) is on the LATEST
                     turn: Decider only detects the checkable figure; Bedrock checks it
    open_question    a gold unanswered_question (pos or neg) is asked on the LATEST turn
    answered_prior   (only while a question is pending) its answer turn is <= LATEST
    agenda_item      the turn's agenda item, or off_agenda inside a drift span / aside

Each window also records `hard_neg`: the categories whose planted near-miss is on
this turn, so calibration on hard negatives can be reported separately.

The state is rendered by the same MeetingState the agent uses; the pending question
and ALREADY FLAGGED are simulated from gold (an oracle agent), which is the right
input for evaluating the questions in isolation.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

from pydantic import BaseModel

from interjection_policy import OFF_AGENDA

from .schema import Meeting
from .state import MeetingState, Pending

PENDING_TICKS = 3  # how long the agent keeps a question pending before giving up


class Window(BaseModel):
    meeting_id: str
    tick: int                 # == turn index of LATEST
    t: float
    state: str
    labels: dict[str, bool | str]
    hard_neg: list[str] = []
    event_ids: list[str] = []


def _offagenda_turns(m: Meeting) -> set[int]:
    out: set[int] = set()
    for g in m.gold:
        if g.category == "off_topic_drift":
            out.update(range(g.turn_index, g.turn_index + max(1, g.span_turns)))
    return out


def windows(m: Meeting) -> Iterator[Window]:
    st = MeetingState(m.cast.pack)
    off = _offagenda_turns(m)
    at: dict[int, list] = {}
    for g in m.gold:
        at.setdefault(g.turn_index, []).append(g)
    questions = {g.turn_index: g for g in m.gold if g.category == "unanswered_question"}

    for tt in m.timeline:
        i = tt.turn_index
        st.add(tt.speaker, tt.text, tt.end_s)
        here = at.get(i, [])
        pos = {g.category for g in here if g.polarity == "pos"}
        anyp = {g.category for g in here}
        labels: dict[str, bool | str] = {
            "action_item": "action_item" in pos,
            "decision_made": "decision_made" in pos,
            "factual_claim": "factual_claim" in anyp,
            "open_question": "unanswered_question" in anyp,
            "agenda_item": OFF_AGENDA if i in off else m.turns[i].agenda_item,
        }
        if st.pending is not None:
            q = questions.get(st.pending.turn_index)
            labels["answered_prior"] = bool(q and q.resolution_turn is not None and q.resolution_turn <= i)
        yield Window(meeting_id=m.meeting_id, tick=i, t=tt.end_s, state=st.render(), labels=labels,
                     hard_neg=sorted({g.category for g in here if g.polarity == "neg"}),
                     event_ids=[g.event_id for g in here])

        # Oracle agent bookkeeping for the next tick.
        for g in here:
            if g.polarity == "pos" and g.category in ("action_item", "decision_made"):
                st.flag(f"{'ACTION' if g.category == 'action_item' else 'DECISION'} {tt.speaker}: {tt.text}")
        if st.pending is not None:
            st.pending.ticks += 1
            if labels.get("answered_prior") or st.pending.ticks > PENDING_TICKS:
                st.pending = None
        if i in questions and st.pending is None:
            st.pending = Pending(tt.speaker, tt.text, i, tt.end_s)


def load_meetings(root: Path) -> list[Meeting]:
    return [Meeting.model_validate_json(p.read_text(encoding="utf-8"))
            for p in sorted(root.glob("*/meeting.json"))]


def write_windows(meetings: list[Meeting], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for m in meetings:
            for w in windows(m):
                fh.write(w.model_dump_json() + "\n")
                n += 1
    return n


def read_windows(path: Path) -> list[Window]:
    return [Window.model_validate(json.loads(line)) for line in path.read_text(encoding="utf-8").splitlines()]
