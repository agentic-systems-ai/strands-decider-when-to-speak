"""Authored meetings: a compact, human-readable transcript format -> Meeting (with gold labels).

The prebuilt dataset is written in this format (by a Claude Code session, see docs/DATA.md)
instead of being generated call-by-call on Bedrock. Labels still come by construction: the
author plants every event and hard near-miss inline, and `lint()` checks the result.

    ---
    <YAML: meeting_id, theme, domain_pack, drama, seed, pack{title, org, agenda, facts}, personas>
    ---
    ## launch_date :: beat summary for this agenda section
    Maya: I'll send the deck to legal by Friday. {action+}
    Raj: Someone should probably look at the deck at some point. {action-}
    Priya: Crash-free was like ninety-seven percent last week. {claim+ F3 "97%"}
    Dev: Crash-free was 99.2, same as the sheet. {claim- F3}
    Maya: Who owns the vendor contract? {question+}
    Raj: Did QA sign off on the build? {question- @+1}
    Priya: Yeah, Lena signed off this morning.
    Dev: Did anyone catch the game last night? {drift+ 3}
    Maya: Okay, June 3rd it is. That's final. {decision+}
    Raj: Maybe June 3rd? Let's sit on it. {decision-}
    Dev: So what I was trying to say is that the—

Tags (end of line, several allowed):
    action+/-     a personal commitment (pos) / a vague, ownerless "someone should" (neg)
    decision+/-   the group settles something (pos) / tentative, nothing settled (neg)
    claim+ F# "v" a checkable figure that contradicts fact F# (pos, claimed value v)
    claim- F#     the same figure quoted correctly (neg: checkable, but nothing to correct)
    question+     a question to the group that is never answered (pos)
    question- @+N a question answered N turns later (neg)
    drift+ N      an off-agenda run starting here, N turns long (pos)
    drift- N      a short aside that returns to the agenda by itself (neg, default 1)
{~} marks a line the author reviewed and deliberately left untagged (silences the question/commitment/
decision heuristics); {~nc} also says it states no fact-sheet figure (silences the figure checks).
A line ending in an em dash (—) was cut off by the next speaker.
Lines starting with a single '#' are comments.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .schema import (
    AgendaItem,
    Beat,
    BeatSheet,
    Cast,
    GoldEvent,
    Meeting,
    MeetingPack,
    Persona,
    Turn,
)
from .timing import build_timeline

VOICES = {
    "female": ["Joanna", "Amy", "Olivia", "Kajal", "Ruth", "Ayanda", "Danielle", "Niamh"],
    "male": ["Matthew", "Brian", "Stephen", "Gregory", "Arthur", "Kevin"],
}
AVATAR_COLORS = ["#E4572E", "#17BEBB", "#FFC914", "#76B041", "#9B5DE5", "#F15BB5"]

TAG_CATEGORY = {"action": "action_item", "decision": "decision_made", "claim": "factual_claim",
                "question": "unanswered_question", "drift": "off_topic_drift"}
_TAG = re.compile(r"\{(action|decision|claim|question|drift)([+-])([^}]*)\}")
_LINE = re.compile(r"^([A-Z][\w.'-]*(?: [A-Z][\w.'-]*)?):\s+(.+)$")
_SECTION = re.compile(r"^##\s+([\w-]+)\s*(?:::\s*(.*))?$")


# Heuristics for lines that look like an event but carry no tag (lint warnings, not errors).
_TAG_QUESTION = "".join(f"(?<!{w})" for w in ("you know", "yeah", "okay", " no", "huh", " eh"))
_MONTHS = ("january", "february", "march", "april", "may", "june", "july", "august", "september",
           "october", "november", "december")
_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
         "sixteen seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def _words(n: int) -> str:
    """Spoken form of 0 <= n < 1,000,000 ('sixty-four', 'eighteen thousand four hundred')."""
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("-" + _ONES[n % 10] if n % 10 else "")
    if n < 1000:
        return _ONES[n // 100] + " hundred" + (" " + _words(n % 100) if n % 100 else "")
    return _words(n // 1000) + " thousand" + (" " + _words(n % 1000) if n % 1000 else "")


_ORD = {"one": "first", "two": "second", "three": "third", "five": "fifth", "eight": "eighth",
        "nine": "ninth", "twelve": "twelfth"}


def _ordinal(n: int) -> str:
    w = _words(n)
    head, _, last = w.rpartition("-")
    last = _ORD.get(last, last[:-1] + "ieth" if last.endswith("y") else last + "th")
    return f"{head}-{last}" if head else last


def spoken_forms(value: str) -> tuple[set[str], set[str]]:
    """(strong, weak) ways a fact-sheet value may be said aloud.

    strong forms are specific enough to flag anywhere ("sixty-four", "twelve six", "august",
    "the twenty-fifth"); weak forms ("four", "the second", "half two") only near a line that
    is already tagged with the same fact (a restatement)."""
    v = value.lower()
    strong: set[str] = set()
    weak: set[str] = set()
    months = [m for m in _MONTHS if m in v]
    strong.update(months)
    if m := re.search(r"(\d{1,2}):(\d\d)", v):  # a time: "2:30 pm"
        h, mm = int(m.group(1)), int(m.group(2))
        weak.update({_words(h), f"{_words(h)} {_words(mm)}" if mm else f"{_words(h)} o'clock"})
        if mm == 30:
            weak.update({f"half {_words(h)}", f"half past {_words(h)}"})
        strong.add(f"{h}:{m.group(2)}")
        return strong, weak
    for num in re.findall(r"\d[\d,]*(?:\.\d+)?", v):
        whole, _, frac = num.replace(",", "").partition(".")
        (strong if len(whole) > 1 or frac else weak).add(num)
        if not whole.isdigit() or int(whole) >= 1_000_000:
            continue
        n = int(whole)
        if months:  # a day of the month
            strong.update({f"the {_ordinal(n)}"} if n >= 10 else set())
            weak.update({_ordinal(n), _words(n)})
            continue
        if frac:  # "zero point six", "ninety-nine point two"
            strong.add(f"{_words(n)} point {' '.join(_words(int(d)) for d in frac)}")
        (strong if n >= 10 else weak).add(_words(n))
        if n >= 1000 and n % 1000 == 0:
            strong.add(f"{_words(n // 1000)} thousand")
        if n >= 1000 and n % 1000 == 0:  # "$25,000" / "15,000" said as "twenty-five" / "fifteen"
            weak.add(_words(n // 1000))
        if 1000 < n < 10000 and n % 100 == 0:
            strong.add(f"{_words(n // 100)} hundred")  # "eighteen hundred"
        if n >= 1000 and (n % 1000) % 100 == 0 and n % 1000:  # "twelve six" = 12,600
            strong.add(f"{_words(n // 1000)} {_words((n % 1000) // 100)}")
        if 100 < n < 1000 and n % 100:  # "three eighty" = 380
            strong.add(f"{_words(n // 100)} {_words(n % 100)}")
    for w in list(strong):  # "a hundred and twelve"
        if "hundred " in w:
            strong.add(w.replace("hundred ", "hundred and "))
    for w in list(strong):
        if w.startswith("one "):
            strong.add("a " + w[4:])
    return strong, weak


def fact_tokens(facts) -> set[str]:
    """Strong spoken forms of every fact-sheet value ('64', 'sixty-four', 'august', ...)."""
    out: set[str] = set()
    for f in facts:
        out |= spoken_forms(f.value)[0]
    return out


def _says(tokens, text: str) -> list[str]:
    low = text.lower()
    return sorted(t for t in tokens if re.search(rf"(?<![\w-]){re.escape(t)}(?![\w-])", low))


_DEFLECT = re.compile(r"\b(hold that|later|come back to|next week|let's see|park)\b", re.I)
_MIC_CHECK = re.compile(r"\b(coming through|can you hear|hear me|see my screen|frozen|on mute|you're muted)\b", re.I)
_REQUEST = re.compile(r"\b(could|can|would|will) you\b[^?]*\?|\bwho can\b[^?]*\?", re.I)
RESTATE_WINDOW = 4  # turns after a tagged fact in which its weak forms count as a restatement


_SUSPECTS = [
    ("unanswered_question", re.compile(rf"{_TAG_QUESTION}\?", re.I), "question"),
    ("action_item", re.compile(r"\b(I'll|I will|I can (?:take|come|do|run|help|cover|handle|draft|bring|write|"
                               r"send|check|call)|I'm going to|I'll take|will do|sure, sure)\b",
                               re.I), "commitment"),
    ("factual_claim", re.compile(r"\d|\b(hundred|thousand|percent|million)\b", re.I), "figure"),
    ("decision_made", re.compile(r"\b(decided|that's final|we're going with|let's go with|it's settled)\b",
                                 re.I), "decision"),
]


class AuthoringError(ValueError):
    pass


@dataclass
class _Tag:
    kind: str
    polarity: str
    args: str


@dataclass
class _Line:
    speaker: str
    text: str
    agenda_item: str
    tags: list[_Tag] = field(default_factory=list)
    lineno: int = 0
    reviewed: bool = False
    noclaim: bool = False


def _split_front_matter(src: str) -> tuple[dict, str]:
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", src, re.S)
    if not m:
        raise AuthoringError("missing YAML front matter between --- lines")
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def parse(src: str) -> tuple[dict, list[tuple[str, str]], list[_Line]]:
    meta, body = _split_front_matter(src)
    sections: list[tuple[str, str]] = []
    lines: list[_Line] = []
    for n, raw in enumerate(body.splitlines(), start=1):
        s = raw.strip()
        if not s or (s.startswith("#") and not s.startswith("##")):
            continue
        if m := _SECTION.match(s):
            sections.append((m.group(1), (m.group(2) or "").strip()))
            continue
        m = _LINE.match(s)
        if not m:
            raise AuthoringError(f"line {n}: expected 'Speaker: text', got {s[:60]!r}")
        if not sections:
            raise AuthoringError(f"line {n}: transcript line before the first '## agenda_id' section")
        text = m.group(2)
        noclaim = "{~nc}" in text
        reviewed = "{~}" in text or noclaim
        text = text.replace("{~nc}", "").replace("{~}", "")
        tags = [_Tag(t.group(1), t.group(2), t.group(3).strip()) for t in _TAG.finditer(text)]
        text = " ".join(_TAG.sub("", text).split())
        if "{" in text or "}" in text:
            raise AuthoringError(f"line {n}: malformed tag in {text[:80]!r}")
        lines.append(_Line(m.group(1), text, sections[-1][0], tags, n, reviewed, noclaim))
    return meta, sections, lines


def _personas(meta: dict, seed: int) -> list[Persona]:
    rng = random.Random(seed)
    pools = {g: rng.sample(v, len(v)) for g, v in VOICES.items()}
    out = []
    for i, p in enumerate(meta["personas"]):
        p = dict(p)
        gender = p.pop("voice_gender", "female")
        if not p.get("polly_voice"):
            pool = pools[gender] or pools["female" if gender == "male" else "male"]
            p["polly_voice"] = pool.pop(0)
        p.setdefault("avatar_color", AVATAR_COLORS[i % len(AVATAR_COLORS)])
        out.append(Persona(**p))
    return out


def build(src: str, *, source_name: str = "") -> Meeting:
    meta, sections, lines = parse(src)
    seed = int(meta.get("seed", 0))
    personas = _personas(meta, seed)
    pack = MeetingPack.model_validate(meta["pack"])
    names = {p.name for p in personas}
    agenda_ids = {a.id for a in pack.agenda}
    facts = {f.id: f for f in pack.facts}

    turns: list[Turn] = []
    gold: list[GoldEvent] = []
    n_ev = 0
    for i, ln in enumerate(lines):
        where = f"{source_name} line {ln.lineno}"
        if ln.speaker not in names:
            raise AuthoringError(f"{where}: unknown speaker {ln.speaker!r} (cast: {sorted(names)})")
        if ln.agenda_item not in agenda_ids:
            raise AuthoringError(f"{where}: unknown agenda id {ln.agenda_item!r}")
        interrupted = ln.text.endswith("—")
        turn = Turn(index=i, speaker=ln.speaker, text=ln.text, agenda_item=ln.agenda_item,
                    interrupted=interrupted)
        for tg in ln.tags:
            n_ev += 1
            ev = GoldEvent(event_id=f"E{n_ev:03d}", category=TAG_CATEGORY[tg.kind],
                           polarity="pos" if tg.polarity == "+" else "neg", turn_index=i,
                           speaker=ln.speaker, agenda_item=ln.agenda_item)
            args = tg.args
            if tg.kind == "claim":
                m = re.match(r'^(F\d+)\s*(?:"([^"]+)")?$', args)
                if not m or m.group(1) not in facts:
                    raise AuthoringError(f"{where}: claim needs a known fact id, got {args!r}")
                ev.fact_id = m.group(1)
                ev.claimed_value = m.group(2) or facts[ev.fact_id].value
                if ev.polarity == "pos" and not m.group(2):
                    raise AuthoringError(f"{where}: claim+ needs the claimed (wrong) value in quotes")
            elif tg.kind == "question":
                m = re.match(r"^@\+(\d+)$", args)
                if ev.polarity == "neg":
                    if not m:
                        raise AuthoringError(f"{where}: question- needs '@+N' (answered N turns later)")
                    ev.resolution_turn = i + int(m.group(1))
                    if ev.resolution_turn >= len(lines):
                        raise AuthoringError(f"{where}: answer turn is past the end of the meeting")
                elif args:
                    raise AuthoringError(f"{where}: question+ takes no arguments (it is never answered)")
            elif tg.kind == "drift":
                ev.span_turns = int(args) if args else (3 if ev.polarity == "pos" else 1)
            elif args:
                raise AuthoringError(f"{where}: {tg.kind} takes no arguments")
            gold.append(ev)
            turn.event_ids.append(ev.event_id)
        turns.append(turn)

    timeline = build_timeline(turns, personas, seed=seed)
    # Align the agenda schedule with when each section actually ran (the meeting "ran to plan"),
    # so the state header's AGENDA ITEM is right outside planted drift.
    ends: dict[str, float] = {}
    for tt, turn in zip(timeline, turns):
        ends[turn.agenda_item] = tt.end_s
    prev = 0.0
    for a in pack.agenda:
        if a.id in ends:
            a.timebox_min = round(max(0.1, (ends[a.id] - prev) / 60), 2)
            prev = ends[a.id]

    beats = BeatSheet(beats=[
        Beat(agenda_item=aid, summary=summary, n_turns=sum(t.agenda_item == aid for t in turns),
             events=[])
        for aid, summary in sections])
    config = {k: meta[k] for k in ("theme", "domain_pack", "drama", "seed") if k in meta}
    config.update(duration_min=round(timeline[-1].end_s / 60, 1) if timeline else 0,
                  participants=len(personas), source="authored", author=meta.get("author", ""),
                  reviewed_untagged=[i for i, ln in enumerate(lines) if ln.reviewed],
                  reviewed_noclaim=[i for i, ln in enumerate(lines) if ln.noclaim])
    return Meeting(meeting_id=meta["meeting_id"], config=config,
                   cast=Cast(theme=meta.get("theme", ""), personas=personas, pack=pack),
                   beats=beats, turns=turns, gold=gold, timeline=timeline)


def lint(m: Meeting) -> list[str]:
    """Warnings about an authored meeting that parses but may be a weak dataset item."""
    out: list[str] = []
    for a, b in zip(m.turns, m.turns[1:]):
        if a.speaker == b.speaker:
            out.append(f"turn {b.index}: {b.speaker} speaks twice in a row")
    for g in m.gold:
        t = m.turns[g.turn_index]
        if g.category == "factual_claim" and g.polarity == "pos":
            fact = next(f for f in m.cast.pack.facts if f.id == g.fact_id)
            if g.claimed_value == fact.value:
                out.append(f"turn {t.index}: claim+ value equals the fact sheet ({fact.value})")
        if g.category == "unanswered_question" and "?" not in t.text:
            out.append(f"turn {t.index}: question event without a '?'")
        if g.category == "unanswered_question" and _MIC_CHECK.search(t.text):
            out.append(f"turn {t.index}: mic/tech check tagged as a question (leave untagged with {{~}})")
        reviewed_q = t.index in m.config.get("reviewed_untagged", [])
        if (g.category == "unanswered_question" and g.polarity == "pos" and not reviewed_q
                and t.index + 1 < len(m.turns)):
            nxt = m.turns[t.index + 1]
            if nxt.speaker != t.speaker and not nxt.text.rstrip().endswith("?") and not nxt.interrupted:
                out.append(f"turn {t.index}: question+ - does the next line answer it? (confirm with {{~}}) "
                           f"[{nxt.speaker}] {nxt.text[:50]}")
        if g.category == "off_topic_drift" and g.polarity == "neg":
            after = g.turn_index + g.span_turns
            if (after < len(m.turns) and len(m.turns[after].text.split()) < 8
                    and m.turns[after].speaker != m.turns[after - 1].speaker
                    and after not in m.config.get("reviewed_untagged", [])):
                out.append(f"turn {t.index}: aside - is the short reply at turn {after} part of it? "
                           f"[{m.turns[after].speaker}] {m.turns[after].text[:40]}")
        if g.category == "factual_claim" and g.polarity == "pos" and g.claimed_value:
            strong, weak = spoken_forms(g.claimed_value)
            for j in range(t.index + 1, min(len(m.turns), t.index + 1 + RESTATE_WINDOW)):
                if j in m.config.get("reviewed_noclaim", []):
                    continue
                if not any(x.turn_index == j and x.category == "factual_claim" for x in m.gold) \
                        and (said := _says(strong | weak, m.turns[j].text)):
                    out.append(f"turn {j}: repeats the wrong {g.fact_id} value {said} without a claim tag? "
                               f"[{m.turns[j].speaker}] {m.turns[j].text[:50]}")
        if g.category == "off_topic_drift" and g.turn_index + g.span_turns > len(m.turns):
            out.append(f"turn {t.index}: drift runs past the end")
        if g.category == "unanswered_question" and g.resolution_turn is not None:
            self_assigned = any(a.turn_index == g.resolution_turn and a.polarity == "pos"
                                and a.category in ("action_item", "decision_made") for a in m.gold)
            for x in m.gold:  # an earlier line already answers it with a commitment or decision
                if g.resolution_turn in m.config.get("reviewed_untagged", []):
                    break
                if (g.turn_index < x.turn_index < g.resolution_turn and x.polarity == "pos"
                        and x.category in ("action_item", "decision_made")
                        and m.turns[x.turn_index].speaker != t.speaker):
                    out.append(f"turn {t.index}: @+N skips an earlier answer at turn {x.turn_index}?")
                    break
            ans = m.turns[g.resolution_turn].text
            ans_ok = g.resolution_turn in m.config.get("reviewed_untagged", [])
            if ans.rstrip().endswith("?") and not ans_ok:
                out.append(f"turn {t.index}: the @+N answer line is itself a question: {ans[:50]}")
            if _DEFLECT.search(ans) and not ans_ok:
                out.append(f"turn {t.index}: the @+N answer line looks like a deferral: {ans[:50]}")
            if m.turns[g.resolution_turn].speaker == t.speaker and not self_assigned:
                out.append(f"turn {t.index}: question is 'answered' by the asker at turn {g.resolution_turn}")
            for d in m.gold:
                end = d.turn_index + d.span_turns
                if (d.category == "off_topic_drift" and d.turn_index <= g.turn_index < end
                        and g.resolution_turn >= end):
                    out.append(f"turn {t.index}: question inside a drift is answered at turn "
                               f"{g.resolution_turn}, outside the span (extend the drift?)")
    tokens = fact_tokens(m.cast.pack.facts)
    tagged: dict[int, set[str]] = {}
    for g in m.gold:
        tagged.setdefault(g.turn_index, set()).add(g.category)
    facts = {f.id: f for f in m.cast.pack.facts}
    claim_at: dict[int, set[str]] = {}
    for g in m.gold:
        if g.category == "factual_claim":
            claim_at.setdefault(g.turn_index, set()).add(g.fact_id)
    for t in m.turns:
        if len(t.text.split()) > 90:
            out.append(f"turn {t.index}: very long line ({len(t.text.split())} words)")
        cats = tagged.get(t.index, set())
        reviewed = t.index in m.config.get("reviewed_untagged", [])
        noclaim = t.index in m.config.get("reviewed_noclaim", [])
        # A restatement of a fact tagged in the last few turns, in any spoken form (even "four").
        recent = {fid for i in range(max(0, t.index - RESTATE_WINDOW), t.index) for fid in claim_at.get(i, ())}
        for fid in sorted(recent - claim_at.get(t.index, set())) if not noclaim else ():
            strong, weak = spoken_forms(facts[fid].value)
            if said := _says(strong | weak, t.text):
                out.append(f"turn {t.index}: restates {fid} {said} without a claim tag? "
                           f"[{t.speaker}] {t.text[:60]}")
        prev = m.turns[t.index - 1] if t.index else None
        if (prev and prev.speaker != t.speaker and _REQUEST.search(prev.text)
                and "action_item" not in cats and not reviewed):
            out.append(f"turn {t.index}: reply to a request (accept = action+, decline = untagged/{{~}})? "
                       f"[{t.speaker}] {t.text[:60]}")
        if "factual_claim" not in cats and not noclaim and (said := _says(tokens, t.text)):
            out.append(f"turn {t.index}: fact-sheet value {said} said without a claim tag? "
                       f"[{t.speaker}] {t.text[:60]}")
        if reviewed:
            continue
        for cat, pattern, what in _SUSPECTS:
            if cat not in cats and pattern.search(t.text):
                out.append(f"turn {t.index}: untagged {what}? [{t.speaker}] {t.text[:70]}")

    have = {(g.category, g.polarity) for g in m.gold}
    for cat in TAG_CATEGORY.values():
        if (cat, "pos") not in have:
            out.append(f"no {cat} positive")
    return out


def load_authored(root: Path) -> list[Meeting]:
    return [build(p.read_text(encoding="utf-8"), source_name=p.name) for p in sorted(root.glob("*.md"))]
