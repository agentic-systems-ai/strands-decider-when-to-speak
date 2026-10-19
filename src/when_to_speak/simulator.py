"""The meeting simulator ("Writers' Room"), stages 1-5.

    casting -> beat sheet (planted events = gold labels) -> improv render (one LLM call
    per turn) -> audit (independent labeller; re-render or drop) -> timing

Labels come by construction: the director plants each event (positives and hard
negatives) and the audit pass keeps them honest. All LLM calls are cached on disk.
"""

from __future__ import annotations

import math
import random
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from .llm import LLM
from .schema import (
    AgendaItem,
    Beat,
    BeatSheet,
    Cast,
    GoldEvent,
    Meeting,
    MeetingPack,
    Persona,
    PlannedEvent,
    Turn,
)
from .timing import build_timeline

PROMPTS = Path(__file__).resolve().parents[2] / "data" / "prompts"
TURNS_PER_MIN = 9.0
CONTEXT_TURNS = 12

# Positive mix per category; hard negatives mirror it 1:1.
CATEGORY_WEIGHTS = {"action_item": 3, "decision_made": 2, "factual_claim": 3,
                    "unanswered_question": 2, "off_topic_drift": 1}

# Polly English voices (neural), by gender, mixed accents.
VOICES = {
    "female": ["Joanna", "Amy", "Olivia", "Kajal", "Ruth", "Ayanda", "Danielle", "Niamh"],
    "male": ["Matthew", "Brian", "Stephen", "Gregory", "Arthur", "Kevin"],
}
AGENT_VOICE = "Aria"  # the facilitator's own voice (NZ English)
AVATAR_COLORS = ["#E4572E", "#17BEBB", "#FFC914", "#76B041", "#9B5DE5", "#F15BB5"]


def _prompt(name: str) -> str:
    return (PROMPTS / f"{name}.md").read_text(encoding="utf-8")


def _fmt(template: str, **kw: object) -> str:
    """str.format that leaves unknown {braces} alone."""
    return re.sub(r"\{(\w+)\}", lambda m: str(kw.get(m.group(1), m.group(0))), template)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]


# ------------------------------------------------------------------ config


class SimConfig(BaseModel):
    theme: str
    duration_min: float = 20
    participants: int = 4
    drama: float = Field(0.6, ge=0, le=1)
    domain_pack: str = "general"
    seed: int = 0

    @property
    def meeting_id(self) -> str:
        return f"{slug(self.theme)}-d{int(self.drama * 10)}-s{self.seed}"


# ------------------------------------------------------------------ stage 1: casting


class PersonaDraft(BaseModel):
    name: str
    role: str
    goals: str
    hidden_agenda: str
    verbosity: int = Field(ge=1, le=5)
    wpm: int = Field(ge=110, le=190)
    catchphrases: list[str] = []
    knows: list[str] = []
    doesnt_know: list[str] = []
    voice_gender: Literal["female", "male"]


class CastDraft(BaseModel):
    personas: list[PersonaDraft]
    pack: MeetingPack


def cast_meeting(llm: LLM, cfg: SimConfig) -> Cast:
    n_agenda = max(3, min(5, round(cfg.duration_min / 5)))
    user = _fmt(_prompt("casting"), participants=cfg.participants, n_agenda=n_agenda,
                duration_min=cfg.duration_min, n_facts=12, theme=cfg.theme,
                domain_pack=cfg.domain_pack, drama=cfg.drama)
    draft = llm.structured("You design realistic fictional meetings. Output via the tool.",
                           user + f"\n(seed {cfg.seed})", CastDraft, name="submit_cast",
                           max_tokens=4096)
    rng = random.Random(cfg.seed)
    pools = {g: rng.sample(v, len(v)) for g, v in VOICES.items()}
    personas = []
    for i, p in enumerate(draft.personas[: cfg.participants]):
        pool = pools[p.voice_gender] or pools["female" if p.voice_gender == "male" else "male"]
        voice = pool.pop(0)
        personas.append(Persona(**p.model_dump(exclude={"voice_gender"}), polly_voice=voice,
                                avatar_color=AVATAR_COLORS[i % len(AVATAR_COLORS)]))
    return Cast(theme=cfg.theme, personas=personas, pack=draft.pack)


# ------------------------------------------------------------------ stage 2: beat sheet


class FollowUpDraft(BaseModel):
    after_turns: int = Field(ge=1, le=6)
    speaker: str
    direction: str


class EventDraft(BaseModel):
    category: Literal["action_item", "decision_made", "factual_claim", "unanswered_question",
                      "off_topic_drift"]
    polarity: Literal["pos", "neg"]
    speaker: str
    beat_turn: int
    direction: str
    fact_id: str | None = None
    claimed_value: str | None = None
    followups: list[FollowUpDraft] = []


class BeatDraft(BaseModel):
    summary: str
    n_turns: int = Field(ge=1)


class AgendaPlanDraft(BaseModel):
    beats: list[BeatDraft]
    events: list[EventDraft]


@dataclass
class TurnPlan:
    index: int
    agenda_item: str
    beat: str
    speaker: str | None = None
    direction: str | None = None
    event_ids: list[str] = field(default_factory=list)


def _event_quota(cfg: SimConfig, rng: random.Random) -> list[tuple[str, str]]:
    n_pos = max(len(CATEGORY_WEIGHTS), round(cfg.duration_min * 60 / 90))
    bag = [c for c, w in CATEGORY_WEIGHTS.items() for _ in range(w)]
    cats = list(CATEGORY_WEIGHTS)  # every category at least once
    while len(cats) < n_pos:
        cats.append(rng.choice(bag))
    events = [(c, "pos") for c in cats] + [(c, "neg") for c in cats]
    rng.shuffle(events)
    return events


def _cast_text(cast: Cast) -> str:
    people = "\n".join(f"- {p.name} ({p.role}): goals: {p.goals}. Hidden agenda: {p.hidden_agenda}. "
                       f"Verbosity {p.verbosity}/5." for p in cast.personas)
    agenda = "\n".join(f"- {a.id}: {a.title} - {a.goal} ({a.timebox_min:g} min)" for a in cast.pack.agenda)
    facts = "\n".join(f"- {f.id} [{f.key}]: {f.statement}" for f in cast.pack.facts)
    return f"MEETING: {cast.pack.title} ({cast.pack.org})\nPEOPLE:\n{people}\nAGENDA:\n{agenda}\nFACT SHEET:\n{facts}"


def plan_beats(llm: LLM, cfg: SimConfig, cast: Cast) -> tuple[BeatSheet, list[TurnPlan], list[PlannedEvent]]:
    rng = random.Random(cfg.seed * 7919 + 1)
    total_turns = round(cfg.duration_min * TURNS_PER_MIN)
    agenda = cast.pack.agenda
    total_box = sum(a.timebox_min for a in agenda) or 1
    turns_per_item = [max(12, round(total_turns * a.timebox_min / total_box)) for a in agenda]

    # Spread the event quota over agenda items in proportion to their turns.
    quota = _event_quota(cfg, rng)
    per_item: list[list[tuple[str, str]]] = [[] for _ in agenda]
    weights = [t for t in turns_per_item]
    for i, ev in enumerate(quota):
        # Greedy: the item with the most free turns per planted event so far.
        k = max(range(len(agenda)), key=lambda j: weights[j] / (1 + len(per_item[j])) + rng.random() * 0.01)
        per_item[k].append(ev)

    names = [p.name for p in cast.personas]
    beats: list[Beat] = []
    plans: list[TurnPlan] = []
    events: list[PlannedEvent] = []
    cast_txt = _cast_text(cast)

    for item, n_turns, item_events in zip(agenda, turns_per_item, per_item):
        speakers = [rng.choice(names) for _ in item_events]
        ev_lines = "\n".join(f"{i + 1}. {c} / {p} / speaker: {s}"
                             for i, ((c, p), s) in enumerate(zip(item_events, speakers)))
        user = _fmt(_prompt("director"), cast=cast_txt, agenda_id=item.id, agenda_title=item.title,
                    n_beats=max(3, min(6, n_turns // 8)), n_turns=n_turns, events=ev_lines,
                    last_turn=n_turns - 2)
        draft = llm.structured("You are a meticulous meeting director. Output via the tool.",
                               user + f"\n(seed {cfg.seed})", AgendaPlanDraft, name="submit_plan",
                               max_tokens=6000)

        base = len(plans)
        item_plans = [TurnPlan(base + i, item.id, "") for i in range(n_turns)]
        # Beat summaries, stretched or squeezed to fill exactly n_turns.
        b_total = sum(b.n_turns for b in draft.beats) or 1
        cursor = 0
        item_beats: list[Beat] = []
        beat_of: list[int] = []  # turn offset -> index into item_beats
        for j, b in enumerate(draft.beats):
            span = n_turns - cursor if j == len(draft.beats) - 1 else max(1, round(n_turns * b.n_turns / b_total))
            span = max(0, min(span, n_turns - cursor))
            for t in range(cursor, cursor + span):
                item_plans[t].beat = b.summary
            beat_of += [j] * span
            item_beats.append(Beat(agenda_item=item.id, summary=b.summary, n_turns=span))
            cursor += span

        def free_slot(start: int) -> int:
            t = max(1, start)
            while t < len(item_plans) and item_plans[t].direction is not None:
                t += 1
            while t >= len(item_plans):  # ran off the end: extend the item
                item_plans.append(TurnPlan(base + len(item_plans), item.id, item_plans[-1].beat))
            return t

        for e in draft.events:
            if e.speaker not in names:
                e.speaker = rng.choice(names)
            t = free_slot(e.beat_turn)
            eid = f"E{len(events) + 1:03d}"
            item_plans[t].speaker, item_plans[t].direction = e.speaker, e.direction
            item_plans[t].event_ids.append(eid)
            pe = PlannedEvent(event_id=eid, category=e.category, polarity=e.polarity,
                              agenda_item=item.id, speaker=e.speaker, direction=e.direction,
                              target_turn_index=base + t, fact_id=e.fact_id,
                              claimed_value=e.claimed_value)
            for fu in sorted(e.followups, key=lambda f: f.after_turns):
                ft = free_slot(t + fu.after_turns)
                item_plans[ft].speaker = fu.speaker if fu.speaker in names else rng.choice(names)
                item_plans[ft].direction = fu.direction
                item_plans[ft].event_ids.append(eid)
                pe.followup_turns.append(base + ft)
                if e.category == "unanswered_question" and e.polarity == "neg":
                    pe.resolution_turn = base + ft
            if e.category == "off_topic_drift":
                pe.span_turns = 1 + len(e.followups)
            events.append(pe)
            if item_beats:
                item_beats[beat_of[min(t, len(beat_of) - 1)] if beat_of else -1].events.append(pe)
        beats.extend(item_beats)
        plans.extend(item_plans)

    for i, p in enumerate(plans):  # re-index after any extensions
        p.index = i
    return BeatSheet(beats=beats), plans, events


# ------------------------------------------------------------------ stage 3: improv render


def _system_for(cast: Cast) -> str:
    agenda = "\n".join(f"- {a.title}: {a.goal}" for a in cast.pack.agenda)
    facts = "\n".join(f"- {f.statement}" for f in cast.pack.facts)
    people = "\n".join(f"- {p.name}, {p.role}" for p in cast.personas)
    return _fmt(_prompt("improv"), title=cast.pack.title, org=cast.pack.org, agenda=agenda,
                facts=facts, people=people)


def _persona_card(p: Persona) -> str:
    return (f"YOU ARE: {p.name}, {p.role}. Goals: {p.goals}. Hidden agenda: {p.hidden_agenda}. "
            f"Verbosity {p.verbosity}/5. Verbal tics: {', '.join(p.catchphrases) or 'none'}. "
            f"You know: {'; '.join(p.knows) or '-'}. You don't know: {'; '.join(p.doesnt_know) or '-'}.")


def _pick_speaker(rng: random.Random, cast: Cast, prev: str | None) -> str:
    people = [p for p in cast.personas if p.name != prev] or cast.personas
    return rng.choices([p.name for p in people], weights=[p.verbosity for p in people])[0]


def render_turn(llm: LLM, cast: Cast, turns: list[Turn], plan: TurnPlan, *, salt: str = "",
                extra: str = "") -> str:
    persona = next(p for p in cast.personas if p.name == plan.speaker)
    item = next((a for a in cast.pack.agenda if a.id == plan.agenda_item), None)
    recent = "\n".join(f"[{t.speaker}] {t.text}" for t in turns[-CONTEXT_TURNS:]) or "(the meeting is starting)"
    direction = (f"YOUR PRIVATE DIRECTION: {plan.direction}{extra}" if plan.direction else
                 "No special direction: continue the discussion naturally (this is a filler line).")
    user = (f"{_persona_card(persona)}\n\nCURRENT AGENDA ITEM: {item.title if item else plan.agenda_item}\n"
            f"WHERE THE DISCUSSION IS GOING: {plan.beat}\n\nRECENT TRANSCRIPT:\n{recent}\n\n"
            f"{direction}\n\nWrite {persona.name}'s next line only.")
    text = llm.text(_system_for(cast), user, max_tokens=200, salt=salt)
    text = text.strip().strip('"').strip()
    text = re.sub(rf"^\[?{re.escape(persona.name)}\]?:\s*", "", text)
    return " ".join(text.split())


def improv_render(llm: LLM, cfg: SimConfig, cast: Cast, plans: list[TurnPlan],
                  progress: Callable[[int, int], None] | None = None) -> list[Turn]:
    rng = random.Random(cfg.seed * 104729 + 3)
    turns: list[Turn] = []
    for plan in plans:
        prev = turns[-1].speaker if turns else None
        if plan.speaker is None:
            plan.speaker = _pick_speaker(rng, cast, prev)
        text = render_turn(llm, cast, turns, plan)
        # Interruption: the new speaker cuts the previous (filler) line short.
        if (turns and not turns[-1].event_ids and not turns[-1].interrupted
                and rng.random() < cfg.drama * 0.15):
            words = turns[-1].text.split()
            if len(words) >= 8:
                turns[-1].text = " ".join(words[: max(4, int(len(words) * rng.uniform(0.45, 0.75)))]) + "—"
                turns[-1].interrupted = True
        turns.append(Turn(index=plan.index, speaker=plan.speaker, text=text, agenda_item=plan.agenda_item,
                          direction=plan.direction, event_ids=list(plan.event_ids)))
        if progress:
            progress(len(turns), len(plans))
    return turns


# ------------------------------------------------------------------ stage 4: audit


class AuditTag(BaseModel):
    turn_index: int
    category: Literal["action_item", "decision_made", "numeric_claim", "open_question", "off_topic"]
    fact_id: str | None = None
    contradicts_fact_sheet: bool | None = None
    answered_in_turn: int | None = None


class AuditTags(BaseModel):
    tags: list[AuditTag] = []


AUDIT_CHUNK, AUDIT_BEFORE, AUDIT_AFTER = 25, 6, 5


def _audit_system(cast: Cast) -> str:
    agenda = "\n".join(f"- {a.id}: {a.title} - {a.goal}" for a in cast.pack.agenda)
    facts = "\n".join(f"- {f.id}: {f.statement}" for f in cast.pack.facts)
    return _fmt(_prompt("auditor"), title=cast.pack.title, agenda=agenda, facts=facts)


def audit_range(llm: LLM, cast: Cast, turns: list[Turn], lo: int, hi: int, salt: str = "") -> list[AuditTag]:
    a, b = max(0, lo - AUDIT_BEFORE), min(len(turns), hi + AUDIT_AFTER)
    lines = "\n".join(f"{t.index}: [{t.speaker}] {t.text}" for t in turns[a:b])
    user = (f"TRANSCRIPT (turns {a}-{b - 1}):\n{lines}\n\nTARGET range: turns {lo} to {hi - 1} inclusive. "
            f"Tag only turns in the TARGET range.")
    out = llm.structured(_audit_system(cast), user, AuditTags, name="submit_tags",
                         max_tokens=3000, temperature=0.0, salt=salt)
    return [t for t in out.tags if lo <= t.turn_index < hi]


def audit_all(llm: LLM, cast: Cast, turns: list[Turn]) -> list[AuditTag]:
    tags: list[AuditTag] = []
    for lo in range(0, len(turns), AUDIT_CHUNK):
        tags += audit_range(llm, cast, turns, lo, min(len(turns), lo + AUDIT_CHUNK))
    return tags


def _expressed(ev: PlannedEvent, tags: list[AuditTag]) -> bool | None:
    """True/False whether the auditor saw the planted event as intended; None = not checkable."""
    t0 = ev.target_turn_index
    near = [t for t in tags if abs(t.turn_index - t0) <= 1]
    has = lambda cat: [t for t in near if t.category == cat]  # noqa: E731
    pos = ev.polarity == "pos"
    if ev.category in ("action_item", "decision_made"):
        return bool(has(ev.category)) == pos
    if ev.category == "factual_claim":
        claims = has("numeric_claim")
        if not claims:
            return False
        return any(bool(c.contradicts_fact_sheet) == pos for c in claims)
    if ev.category == "unanswered_question":
        qs = has("open_question")
        if not qs:
            return False
        return any((q.answered_in_turn is None) == pos for q in qs)
    if ev.category == "off_topic_drift":
        if not pos:
            return None
        span = range(t0, t0 + ev.span_turns)
        hits = {t.turn_index for t in tags if t.category == "off_topic" and t.turn_index in span}
        return len(hits) >= math.ceil(0.6 * ev.span_turns)
    return None


STRENGTHEN = {
    ("pos", "action_item"): " Make the personal commitment unmistakable: 'I'll ...' with a concrete task.",
    ("pos", "decision_made"): " Make it clearly final and settled for the group.",
    ("pos", "factual_claim"): " State the (wrong) figure explicitly as a fact.",
    ("pos", "unanswered_question"): " Ask it plainly as a question to the whole group.",
    ("neg", "action_item"): " Keep it vague: nobody takes ownership.",
    ("neg", "decision_made"): " Keep it tentative; nothing is settled.",
    ("neg", "factual_claim"): " Quote the figure exactly as the pre-read has it.",
    ("neg", "unanswered_question"): " Ask it plainly as a question to the whole group.",
}


def audit_and_reconcile(llm: LLM, cfg: SimConfig, cast: Cast, turns: list[Turn], plans: list[TurnPlan],
                        events: list[PlannedEvent], max_retries: int = 2) -> tuple[list[AuditTag], list[GoldEvent]]:
    tags = audit_all(llm, cast, turns)
    for ev in events:
        for attempt in range(max_retries + 1):
            ok = _expressed(ev, tags)
            if ok is None or ok:
                break
            if attempt == max_retries or ev.category == "off_topic_drift":
                ev.dropped = True
                break
            t = ev.target_turn_index
            extra = STRENGTHEN.get((ev.polarity, ev.category), "")
            turns[t].text = render_turn(llm, cast, turns[:t], plans[t], salt=f"retry{attempt + 1}", extra=extra)
            lo, hi = max(0, t - 2), min(len(turns), t + 3)
            tags = [x for x in tags if not lo <= x.turn_index < hi] + \
                audit_range(llm, cast, turns, lo, hi, salt=f"retry{attempt + 1}")

    gold: list[GoldEvent] = []
    planted_at: dict[tuple[str, int], PlannedEvent] = {}
    for ev in events:
        if ev.dropped:
            continue
        gold.append(GoldEvent(event_id=ev.event_id, category=ev.category, polarity=ev.polarity,
                              turn_index=ev.target_turn_index, speaker=ev.speaker,
                              agenda_item=ev.agenda_item, fact_id=ev.fact_id, claimed_value=ev.claimed_value,
                              resolution_turn=ev.resolution_turn, span_turns=ev.span_turns))
        for d in (-1, 0, 1):
            planted_at[(ev.category, ev.target_turn_index + d)] = ev

    # Expressed but not planted: add as audit labels. A follow-up turn tagged with its own
    # event's category (the drift continuing, say) is part of that event, not a new one.
    followup_of = {(e.category, ft) for e in events if not e.dropped for ft in e.followup_turns}
    n = 0
    cat_map = {"action_item": "action_item", "decision_made": "decision_made",
               "numeric_claim": "factual_claim", "open_question": "unanswered_question"}
    for tg in sorted(tags, key=lambda x: x.turn_index):
        if tg.category not in cat_map:
            continue
        cat = cat_map[tg.category]
        if (cat, tg.turn_index) in planted_at or (cat, tg.turn_index) in followup_of:
            continue
        if cat == "factual_claim":
            pol = "pos" if tg.contradicts_fact_sheet else "neg"
        elif cat == "unanswered_question":
            pol = "pos" if tg.answered_in_turn is None else "neg"
        else:
            pol = "pos"
        n += 1
        turn = turns[tg.turn_index]
        gold.append(GoldEvent(event_id=f"A{n:03d}", category=cat, polarity=pol, turn_index=tg.turn_index,
                              speaker=turn.speaker, agenda_item=turn.agenda_item, fact_id=tg.fact_id,
                              resolution_turn=tg.answered_in_turn, source="audit"))
        turn.event_ids.append(f"A{n:03d}")

    # Unplanted off-topic runs of 3+ turns.
    off = sorted({t.turn_index for t in tags if t.category == "off_topic"})
    planned_drift = {i for e in events if e.category == "off_topic_drift" and not e.dropped
                     for i in range(e.target_turn_index - 1, e.target_turn_index + e.span_turns + 1)}
    run: list[int] = []
    for i in off + [10 ** 9]:
        if run and i == run[-1] + 1:
            run.append(i)
            continue
        if len(run) >= 3 and not planned_drift.intersection(run):
            n += 1
            gold.append(GoldEvent(event_id=f"A{n:03d}", category="off_topic_drift", polarity="pos",
                                  turn_index=run[0], speaker=turns[run[0]].speaker,
                                  agenda_item=turns[run[0]].agenda_item, span_turns=len(run), source="audit"))
        run = [i]
    gold.sort(key=lambda g: g.turn_index)
    return tags, gold


# ------------------------------------------------------------------ pipeline


def simulate(cfg: SimConfig, llm: LLM | None = None, out_dir: Path | None = None,
             progress: Callable[[str], None] = print) -> Meeting:
    llm = llm or LLM()
    progress(f"[{cfg.meeting_id}] casting")
    cast = cast_meeting(llm, cfg)
    progress(f"[{cfg.meeting_id}] beat sheet")
    beats, plans, events = plan_beats(llm, cfg, cast)
    progress(f"[{cfg.meeting_id}] improv render: {len(plans)} turns, {len(events)} planted events")
    turns = improv_render(llm, cfg, cast, plans)
    progress(f"[{cfg.meeting_id}] audit")
    _, gold = audit_and_reconcile(llm, cfg, cast, turns, plans, events)
    timeline = build_timeline(turns, cast.personas, seed=cfg.seed)
    m = Meeting(meeting_id=cfg.meeting_id, config=cfg.model_dump(), cast=cast, beats=beats,
                turns=turns, gold=gold, timeline=timeline)
    dropped = sum(e.dropped for e in events)
    progress(f"[{cfg.meeting_id}] done: {len(turns)} turns, {len(gold)} gold "
             f"({sum(g.source == 'audit' for g in gold)} from audit), {dropped} dropped, "
             f"{timeline[-1].end_s / 60:.1f} min")
    if out_dir:
        d = out_dir / cfg.meeting_id
        d.mkdir(parents=True, exist_ok=True)
        (d / "meeting.json").write_text(m.model_dump_json(indent=1), encoding="utf-8")
    return m
