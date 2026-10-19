"""Rolling window over a stream, rendered as a Decider state under a token budget.

    <HEADER lines>
    RECENT TRANSCRIPT (oldest->newest):
    [Dana] ...
    [Raj] ...
    >> LATEST: [Mei] ...

Decider latency grows with input length, so the window keeps the newest lines that
fit the budget and drops the oldest. The LATEST marker is what every question
anchors on.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Mapping
from dataclasses import dataclass

LATEST_MARK = ">> LATEST: "


def approx_tokens(text: str) -> int:
    """~3.5 characters per token for English: slightly pessimistic, so we stay under budget."""
    return int(len(text) / 3.5) + 1


@dataclass(frozen=True)
class Line:
    speaker: str
    text: str
    t: float = 0.0

    def render(self) -> str:
        return f"[{self.speaker}] {self.text}"


class RollingWindow:
    def __init__(self, max_tokens: int = 700, max_lines: int = 12, latest_n: int = 1,
                 count_tokens: Callable[[str], int] = approx_tokens):
        self.max_tokens = max_tokens
        self.latest_n = latest_n
        self.count = count_tokens
        self.lines: deque[Line] = deque(maxlen=max_lines)

    def add(self, speaker: str, text: str, t: float = 0.0) -> None:
        self.lines.append(Line(speaker, " ".join(text.split()), t))

    def clear(self) -> None:
        self.lines.clear()

    @staticmethod
    def _header(header: str | Mapping[str, str] | None) -> str:
        if not header:
            return ""
        if isinstance(header, str):
            return header.rstrip() + "\n"
        return "".join(f"{k}: {v}\n" for k, v in header.items() if v)

    def render(self, header: str | Mapping[str, str] | None = None) -> str:
        head = self._header(header) + "RECENT TRANSCRIPT (oldest->newest):\n"
        lines = list(self.lines)
        if not lines:
            return head + "(silence)"
        n_latest = min(self.latest_n, len(lines))
        latest = [LATEST_MARK + ln.render() for ln in lines[-n_latest:]]
        budget = self.max_tokens - self.count(head) - sum(self.count(x) for x in latest)
        if budget < 0:
            # The latest line alone is over budget (a long monologue): keep its tail.
            keep_chars = max(40, int((self.max_tokens - self.count(head)) * 3.5) - len(LATEST_MARK) - 8)
            tail = latest[-1][len(LATEST_MARK):][-keep_chars:]
            return head + LATEST_MARK + "..." + tail
        context: list[str] = []
        for ln in reversed(lines[:-n_latest]):
            r = ln.render()
            c = self.count(r)
            if c > budget:
                break
            context.append(r)
            budget -= c
        return head + "\n".join(list(reversed(context)) + latest)
