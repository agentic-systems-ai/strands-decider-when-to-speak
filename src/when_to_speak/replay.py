"""Replay mode A: stream a meeting's timeline as Utterance events.

`speed` = 1.0 is real time; 0 means as fast as possible (evals, CI). Modes B (audio +
Transcribe) and C (live) produce the same Utterance events, so the agent cannot tell
them apart.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Iterator

from .schema import Meeting, Utterance


def utterances(meeting: Meeting) -> Iterator[Utterance]:
    for tt in meeting.timeline:
        yield Utterance(speaker=tt.speaker, text=tt.text, t_start=tt.start_s, t_end=tt.end_s,
                        turn_index=tt.turn_index)


async def text_replay(meeting: Meeting, speed: float = 1.0) -> AsyncIterator[Utterance]:
    """Yield each utterance when it *ends* (that is when a final ASR result would arrive)."""
    loop = asyncio.get_running_loop()
    t0 = loop.time()
    for u in utterances(meeting):
        if speed > 0:
            delay = u.t_end / speed - (loop.time() - t0)
            if delay > 0:
                await asyncio.sleep(delay)
        yield u
