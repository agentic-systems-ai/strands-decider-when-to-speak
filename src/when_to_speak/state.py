"""The meeting state the agent keeps, rendered into a Decider window (spec §3.1).

Shared by the live agent and the offline dataset builder, so evals see exactly the
states the agent sees at runtime.

    AGENDA ITEM (current): launch_date - Pick the public launch date
    FACT SHEET KEYS: crash_free_sessions_last_week, launch_date_candidate, ...
    ALREADY FLAGGED: ACTION Mei: send revised deck to legal (Thu)
    PENDING: [Dana] Who owns the app store screenshots?
    RECENT TRANSCRIPT (oldest->newest):
    [Dana] ...
    >> LATEST: [Mei] ...
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from interjection_policy import RollingWindow, meeting_questions
from decider_client import Question

from .schema import MeetingPack


@dataclass
class Pending:
    speaker: str
    text: str
    turn_index: int | None
    asked_t: float
    ticks: int = 0


class MeetingState:
    def __init__(self, pack: MeetingPack, max_tokens: int = 700, max_lines: int = 10,
                 max_flagged: int = 5):
        self.pack = pack
        self.window = RollingWindow(max_tokens=max_tokens, max_lines=max_lines)
        self.flagged: deque[str] = deque(maxlen=max_flagged)
        self.pending: Pending | None = None
        # Scheduled agenda: cumulative timebox ends in seconds.
        ends, acc = [], 0.0
        for a in pack.agenda:
            acc += a.timebox_min * 60
            ends.append(acc)
        self._ends = ends
        self.now = 0.0
        self.latest = ""

    # ------------------------------------------------------------- updates

    def add(self, speaker: str, text: str, t: float) -> None:
        self.window.add(speaker, text, t)
        self.now = t
        self.latest = text

    def flag(self, line: str) -> None:
        self.flagged.append(" ".join(line.split())[:120])

    # ------------------------------------------------------------- views

    def scheduled_item(self, t: float | None = None) -> int:
        """Index of the agenda item the timebox schedule says is current."""
        t = self.now if t is None else t
        for i, end in enumerate(self._ends):
            if t < end:
                return i
        return len(self._ends) - 1

    def agenda_options(self) -> list[tuple[str, str]]:
        return [(a.id, f"{a.title}: {a.goal}") for a in self.pack.agenda]

    def questions(self) -> list[Question]:
        return meeting_questions(pending_question=self.pending is not None, off_topic=True)

    def render(self) -> str:
        a = self.pack.agenda[self.scheduled_item()]
        header = {
            "AGENDA ITEM (current)": f"{a.id} - {a.title}: {a.goal}",
            "FACT SHEET KEYS": ", ".join(f.key for f in self.pack.facts),
            "ALREADY FLAGGED": "; ".join(self.flagged) or "(none)",
        }
        if self.pending:
            header["PENDING"] = f"[{self.pending.speaker}] {self.pending.text}"
        return self.window.render(header)
