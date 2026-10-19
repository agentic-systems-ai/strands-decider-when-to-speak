"""Stage 5: turn durations, pauses and interruptions -> a timeline."""

from __future__ import annotations

import random

from .schema import Persona, TimedTurn, Turn


def build_timeline(turns: list[Turn], personas: list[Persona], seed: int = 0) -> list[TimedTurn]:
    """duration = words / (wpm / 60); gap 0.2-1.2 s; an interrupted turn is overlapped
    by the next one by 0.3-0.8 s. Overlaps happen only after interrupted turns."""
    rng = random.Random(seed)
    wpm = {p.name: p.wpm for p in personas}
    out: list[TimedTurn] = []
    t = 0.5
    for i, turn in enumerate(turns):
        words = max(1, len(turn.text.split()))
        dur = words / (wpm.get(turn.speaker, 150) / 60.0)
        if i > 0:
            prev = turns[i - 1]
            if prev.interrupted:
                t = max(out[-1].start_s + 0.3, out[-1].end_s - rng.uniform(0.3, 0.8))
            else:
                t = out[-1].end_s + rng.uniform(0.2, 1.2)
        out.append(TimedTurn(turn_index=turn.index, speaker=turn.speaker, text=turn.text,
                             start_s=round(t, 3), end_s=round(t + dur, 3)))
    return out
