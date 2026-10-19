"""Data model shared by the simulator, the replay engine, the agent and the evals.

meeting.json = Cast + MeetingPack + BeatSheet + rendered turns + gold labels + timeline.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Category = Literal["action_item", "decision_made", "factual_claim", "unanswered_question",
                   "off_topic_drift"]
CATEGORIES: tuple[str, ...] = ("action_item", "decision_made", "factual_claim",
                               "unanswered_question", "off_topic_drift")


class Persona(BaseModel):
    name: str
    role: str
    goals: str
    hidden_agenda: str
    verbosity: int = Field(ge=1, le=5)
    wpm: int = Field(ge=110, le=190)
    catchphrases: list[str] = []
    knows: list[str] = []
    doesnt_know: list[str] = []
    polly_voice: str = ""
    avatar_color: str = "#888888"


class AgendaItem(BaseModel):
    id: str            # short slug, used as the Decider choice label
    title: str
    goal: str          # one line
    timebox_min: float


class Fact(BaseModel):
    id: str            # "F7"
    key: str           # "crash_free_sessions_last_week"
    statement: str     # "Crash-free sessions last week = 99.2%"
    value: str         # "99.2%"


class MeetingPack(BaseModel):
    title: str
    org: str           # fictional
    agenda: list[AgendaItem]
    facts: list[Fact]


class Cast(BaseModel):
    theme: str
    personas: list[Persona]
    pack: MeetingPack


class PlannedEvent(BaseModel):
    event_id: str
    category: Category
    polarity: Literal["pos", "neg"]
    agenda_item: str
    speaker: str
    direction: str                     # private stage direction for the improv render
    target_turn_index: int = -1        # filled in when rendered
    fact_id: str | None = None         # factual_claim
    claimed_value: str | None = None   # factual_claim: what the speaker says
    resolution_turn: int | None = None # unanswered_question negatives: where it gets answered
    span_turns: int = 1                # off_topic_drift: how many turns the drift lasts
    followup_turns: list[int] = []     # turns that continue this event (answer, drift lines)
    source: Literal["plan", "audit"] = "plan"
    dropped: bool = False


class Beat(BaseModel):
    agenda_item: str
    summary: str
    n_turns: int
    events: list[PlannedEvent] = []


class BeatSheet(BaseModel):
    beats: list[Beat]


class Turn(BaseModel):
    index: int
    speaker: str
    text: str
    agenda_item: str
    direction: str | None = None       # stage direction used, if any
    event_ids: list[str] = []
    interrupted: bool = False          # this turn was cut off by the next speaker


class TimedTurn(BaseModel):
    turn_index: int
    speaker: str
    text: str
    start_s: float
    end_s: float


class GoldEvent(BaseModel):
    """A label by construction, after the audit pass reconciled it."""

    event_id: str
    category: Category
    polarity: Literal["pos", "neg"]
    turn_index: int
    speaker: str
    agenda_item: str
    fact_id: str | None = None
    claimed_value: str | None = None
    resolution_turn: int | None = None
    span_turns: int = 1
    source: Literal["plan", "audit"] = "plan"


class Meeting(BaseModel):
    meeting_id: str
    config: dict
    cast: Cast
    beats: BeatSheet
    turns: list[Turn]
    gold: list[GoldEvent]
    timeline: list[TimedTurn] = []

    def positives(self, category: str | None = None) -> list[GoldEvent]:
        return [g for g in self.gold if g.polarity == "pos" and (category is None or g.category == category)]


class Utterance(BaseModel):
    """What every replay mode emits; the agent only ever sees these."""

    speaker: str
    text: str
    t_start: float
    t_end: float
    is_final: bool = True
    turn_index: int | None = None      # known in text replay; None for live ASR
