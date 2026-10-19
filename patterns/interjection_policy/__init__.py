"""interjection_policy: should my stream-watching agent speak now, and why?

A reusable Strands Decider pattern. See README.md.
"""

from .policy import Action, PolicyResult, Thresholds, TieredPolicy, signals_from
from .questions import (
    ALREADY_FLAGGED,
    ANSWERED_PRIOR,
    MEETING_CATEGORIES,
    OFF_AGENDA,
    OFF_TOPIC,
    Category,
    make_agenda_question,
    make_interjection_questions,
    meeting_questions,
)
from .strands_wiring import GateResult, InterjectionGate, InterjectionIntervention
from .window import RollingWindow, approx_tokens

__all__ = [
    "Action", "PolicyResult", "Thresholds", "TieredPolicy", "signals_from",
    "ALREADY_FLAGGED", "ANSWERED_PRIOR", "MEETING_CATEGORIES", "OFF_AGENDA", "OFF_TOPIC", "Category",
    "make_agenda_question", "make_interjection_questions", "meeting_questions",
    "GateResult", "InterjectionGate", "InterjectionIntervention",
    "RollingWindow", "approx_tokens",
]
