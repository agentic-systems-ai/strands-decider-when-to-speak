"""Typed questions for the interjection policy.

One yes/no (noul) question per category, all asked against the same window state
in a single Decider call. Separate nouls rather than one big choice, so co-occurring
events (a decision that is also an action item) are both reported.

The window state marks the newest line with `>> LATEST:` (see window.py); every
question asks about the LATEST lines only, which keeps the judgement local.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from decider_client import Question


@dataclass(frozen=True)
class Category:
    """A plain-English event definition. `true`/`false` sharpen the boundary."""

    question: str
    true: str
    false: str


CategorySpec = str | Category | Mapping[str, str]


def _as_category(name: str, spec: CategorySpec) -> Category:
    if isinstance(spec, Category):
        return spec
    if isinstance(spec, str):
        return Category(
            question=f"Do the LATEST lines contain {spec}?",
            true=f"the LATEST lines clearly contain {spec}",
            false=f"the LATEST lines do not contain {spec}, or only something vaguely similar",
        )
    return Category(spec["question"], spec["true"], spec["false"])


def make_interjection_questions(categories: Mapping[str, CategorySpec]) -> list[Question]:
    """Build one noul question per category.

    `categories` maps a key to either a short noun phrase ("a bug report"), a
    `Category`, or a dict with `question`/`true`/`false`.
    """
    out = []
    for key, spec in categories.items():
        c = _as_category(key, spec)
        out.append(Question(key, "noul", c.question, {"true": c.true, "false": c.false}))
    return out


# --------------------------------------------------------------------- meeting defaults

MEETING_CATEGORIES: dict[str, Category] = {
    "action_item": Category(
        "Did someone in the LATEST lines commit to doing a specific task?",
        "a person committed to a concrete task (a named owner and an action)",
        "no commitment, or only a vague suggestion that someone should do something",
    ),
    "decision_made": Category(
        "Did the group reach a final decision in the LATEST lines?",
        "an explicit, settled decision was stated",
        "options were discussed, or the idea is tentative or undecided",
    ),
    "factual_claim": Category(
        "Do the LATEST lines state a specific number, date or metric that could be checked "
        "against the fact sheet?",
        "a specific number, date or metric is stated as fact",
        "no specific checkable number, date or metric is stated",
    ),
    "open_question": Category(
        "Do the LATEST lines ask a question directed at the group that still needs an answer?",
        "a real question is put to the group and is not answered in the same lines",
        "no question, a rhetorical question, or a question answered right away",
    ),
}

ANSWERED_PRIOR = Category(
    "Has the PENDING question been answered in the transcript?",
    "someone gave an answer or assigned an owner for the PENDING question",
    "nobody has answered the PENDING question yet",
)

ALREADY_FLAGGED = Category(
    "Is the LATEST point the same as something listed in ALREADY FLAGGED?",
    "the LATEST point repeats an item already in ALREADY FLAGGED",
    "the LATEST point is new, or ALREADY FLAGGED is empty",
)

OFF_AGENDA = "off_agenda"

# Asked directly, drift is caught far more often than as the off_agenda option of the agenda
# choice, which the Decider almost never picks (dev: recall 0.66 at p>=0.7 vs 0.02).
OFF_TOPIC = Category(
    "Are the LATEST lines an off-topic tangent rather than meeting business?",
    "the LATEST lines are a tangent: chit-chat, news, jokes or personal matters unrelated to the agenda",
    "the LATEST lines discuss the meeting's business",
)


def make_agenda_question(agenda_items: Sequence[tuple[str, str]],
                         key: str = "agenda_item") -> Question:
    """A choice question: which agenda item is being discussed, or off_agenda.

    `agenda_items` is a list of (label, one-line description).
    """
    options = {label: desc for label, desc in agenda_items}
    options[OFF_AGENDA] = "the LATEST lines are about something not on the agenda"
    return Question(key, "choice", "Which agenda item is being discussed in the LATEST lines?",
                    options)


def meeting_questions(agenda_items: Sequence[tuple[str, str]] = (), *,
                      pending_question: bool = False,
                      dedupe: bool = True, off_topic: bool = False) -> list[Question]:
    """The full meeting question set for one tick (spec §3.2).

    `off_topic` adds a yes/no `off_agenda` question; pass no `agenda_items` to drop the choice.
    """
    qs = make_interjection_questions(MEETING_CATEGORIES)
    if pending_question:
        qs += make_interjection_questions({"answered_prior": ANSWERED_PRIOR})
    if agenda_items:
        qs.append(make_agenda_question(agenda_items))
    if off_topic:
        qs += make_interjection_questions({OFF_AGENDA: OFF_TOPIC})
    if dedupe:
        qs += make_interjection_questions({"already_flagged": ALREADY_FLAGGED})
    return qs
