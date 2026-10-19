"""Confidence -> behaviour. Plain Python over Decider's numbers.

    p >= speak            SPEAK   wake the LLM; it may say something out loud
    note <= p < speak     NOTE    silent card, no LLM call
    p < note              SILENT  nothing

Plus three guards that keep the agent from being annoying:

- cooldown:  at most one spoken interjection per `cooldown_s`; extra SPEAKs become NOTEs
- dedupe:    if the dedupe signal (e.g. `already_flagged`) is >= `dedupe_threshold`, SILENT
- streak:    a category can require N consecutive firing ticks (e.g. off-agenda drift)

A category can opt out of the cooldown and dedupe guards (`Thresholds(cooldown=False,
dedupe=False)`) when its wake does silent work too, such as checking a figure or recording a
card; the agent then enforces the cooldown on the spoken line itself.

Thresholds are config: tune them on your own labelled windows with
scripts/tune_thresholds.py.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum

from decider_client import Decision


class Action(str, Enum):
    SPEAK = "speak"
    NOTE = "note"
    SILENT = "silent"


@dataclass(frozen=True)
class Thresholds:
    speak: float = 0.85
    note: float = 0.5
    min_streak: int = 1  # consecutive ticks at >= note before the category may fire
    cooldown: bool = True  # SPEAK is downgraded to NOTE during the cooldown
    dedupe: bool = True    # the dedupe signal can suppress this category


@dataclass
class PolicyResult:
    action: Action
    category: str | None
    confidence: float
    reasons: list[str]
    tiers: dict[str, Action] = field(default_factory=dict)  # per-category tier this tick

    @property
    def wake(self) -> bool:
        return self.action is Action.SPEAK


def signals_from(decisions: Mapping[str, Decision],
                 choice_signals: Mapping[str, tuple[str, str]] | None = None) -> dict[str, float]:
    """Flatten decisions into {signal: probability}.

    Noul questions give P(true) under their own key. `choice_signals` maps a signal
    name to (question key, option label), e.g. {"off_agenda": ("agenda_item", "off_agenda")}.
    """
    out = {k: d.p_true for k, d in decisions.items() if set(d.probs) == {"true", "false"}}
    for name, (qkey, label) in (choice_signals or {}).items():
        if qkey in decisions:
            out[name] = decisions[qkey].probs.get(label, 0.0)
    return out


class TieredPolicy:
    def __init__(self, thresholds: Mapping[str, Thresholds], *,
                 cooldown_s: float = 60.0,
                 dedupe: str | None = "already_flagged",
                 dedupe_threshold: float = 0.7):
        self.thresholds = dict(thresholds)
        self.cooldown_s = cooldown_s
        self.dedupe = dedupe
        self.dedupe_threshold = dedupe_threshold
        self._streak: dict[str, int] = {c: 0 for c in self.thresholds}
        self._last_spoken: float | None = None

    def reset(self) -> None:
        self._streak = {c: 0 for c in self.thresholds}
        self._last_spoken = None

    def record_spoken(self, now: float) -> None:
        """Call when the agent actually spoke, so the cooldown starts from there."""
        self._last_spoken = now

    def in_cooldown(self, now: float) -> bool:
        return self._last_spoken is not None and now - self._last_spoken < self.cooldown_s

    def decide(self, signals: Mapping[str, float], now: float) -> PolicyResult:
        tiers: dict[str, Action] = {}
        reasons: list[str] = []
        for cat, th in self.thresholds.items():
            p = signals.get(cat, 0.0)
            self._streak[cat] = self._streak[cat] + 1 if p >= th.note else 0
            if self._streak[cat] < th.min_streak:
                tier = Action.SILENT
                if p >= th.note:
                    reasons.append(f"{cat}: streak {self._streak[cat]}/{th.min_streak}")
            elif p >= th.speak:
                tier = Action.SPEAK
            elif p >= th.note:
                tier = Action.NOTE
            else:
                tier = Action.SILENT
            tiers[cat] = tier

        rank = {Action.SPEAK: 2, Action.NOTE: 1, Action.SILENT: 0}
        firing = [c for c, t in tiers.items() if t is not Action.SILENT]
        if not firing:
            return PolicyResult(Action.SILENT, None, 0.0, reasons or ["nothing above threshold"], tiers)

        best = max(firing, key=lambda c: (rank[tiers[c]], signals.get(c, 0.0)))
        action, conf = tiers[best], signals.get(best, 0.0)
        reasons.append(f"{best}: p={conf:.2f} -> {action.value}")

        th = self.thresholds[best]
        if self.dedupe and th.dedupe and signals.get(self.dedupe, 0.0) >= self.dedupe_threshold:
            reasons.append(f"suppressed: {self.dedupe}={signals[self.dedupe]:.2f}")
            return PolicyResult(Action.SILENT, best, conf, reasons, tiers)

        if action is Action.SPEAK and th.cooldown and self.in_cooldown(now):
            reasons.append(f"cooldown: spoke {now - self._last_spoken:.0f}s ago -> note")
            action = Action.NOTE

        # A category that fired resets its streak, so a drift nudge is not repeated every tick.
        if action is Action.SPEAK and th.min_streak > 1:
            self._streak[best] = 0
        return PolicyResult(action, best, conf, reasons, tiers)
