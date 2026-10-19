# The dataset

The evaluation set is **prebuilt**: meetings are authored once, by a Claude Code session
(Claude Opus 5.5), in a compact transcript format with inline labels, and committed to the
repo. The Strands + Bedrock experiment then runs over this fixed set, so every run (Decider,
LLM judge, agent) sees the same meetings and nothing in the eval depends on generation-time
randomness or cost.

The online simulator (`src/when_to_speak/simulator.py`, `make pilot`/`make data`) still
exists and produces the same `meeting.json` shape; it is kept for the live demo's "generate a
new meeting" button, not for the eval set.

```
data/authored/<meeting_id>.md      the source (YAML header + tagged transcript)
data/meetings/<id>/meeting.json    built by scripts/build_dataset.py (Meeting schema)
data/windows/{dev,test}.jsonl      one labelled Decider window per utterance
data/windows/split.txt             which meeting is in which split
```

`make dataset` rebuilds everything from the sources; `python scripts/build_dataset.py --check`
parses and lints without writing.

## Format

See the docstring of [`src/when_to_speak/authored.py`](../src/when_to_speak/authored.py).
In short: YAML front matter (cast, agenda, a 12-fact sheet), then `## agenda_id :: beat`
sections of `Speaker: text {tag} {tag}` lines.

| Tag | Meaning | Window labels it drives |
|---|---|---|
| `{action+}` / `{action-}` | personal commitment to a concrete task / vague "someone should" | `action_item` true only for `+` |
| `{decision+}` / `{decision-}` | the group settles something / tentative, parked, "maybe" | `decision_made` true only for `+` |
| `{claim+ F3 "97%"}` / `{claim- F3}` | a fact-sheet figure stated wrongly / stated correctly | `factual_claim` true for both (Decider detects a checkable figure; Bedrock checks it) |
| `{question+}` / `{question- @+N}` | a question to the group that is never answered / answered N turns later | `open_question` true for both; `answered_prior` true from the answer turn |
| `{drift+ N}` / `{drift- N}` | an off-agenda run of N turns / a one-line aside | `agenda_item = off_agenda` on those turns |

Lines ending in `—` were cut off by the next speaker (the timeline overlaps them). `{~}` marks a
line the author reviewed and deliberately left untagged (a proposed date, a rhetorical question);
it only silences the lint heuristics.

## Labelling rules (what keeps the labels honest)

Untagged lines are negatives for every category, so the discipline is in what untagged lines
must **not** contain:

1. **No first-person commitments** ("I'll …", "I can take that", "will do") unless tagged `action+`.
   A request ("send it to me too") is not a commitment; the short acceptance ("sure, sure",
   "will do") is, even when it repeats an earlier commitment.
2. **Nothing settled** unless tagged `decision+`. Positions ("I'd rather the tenth"), parking
   ("let's see what legal says"), process norms ("let's not let the press slot decide") and
   "maybe we…" are tagged `decision-` when they are near-misses.
3. **Every fact-sheet figure stated as fact is tagged** (`claim+` wrong, `claim-` right), including
   casual restatements ("two days, yeah"), spelled-out numbers ("sixty-four"), months ("from March")
   and the repeat right after a correction ("Sixty-four. Okay."). After every `claim+`, check the
   next few lines for repeats. Untagged lines avoid other project metrics ("screenshots are 80%
   done"); incidental numbers (a marathon time, "three screens", a pickup time) are kept rare.
4. **Every genuine question is tagged.** A confirmation question ("…, right?") that gets a real
   answer is a question. Incredulous echoes ("You've what?", "Eighteen hundred for a DJ?") and
   mic checks are not: leave them untagged with `{~}`.
5. **`@+N` must land on a line that answers the specific thing asked**, not a related figure or a
   restatement by the asker. If nobody answers it, it is `question+`, and `question+` must stay
   unanswered for the rest of the meeting.
6. **Drift spans cover every off-agenda turn**, including replies to the aside ("Hi, Mango."), and
   the line that steers back is outside the span.

Hard negatives are planted next to positives in the same meeting: a vague "someone should"
near a real commitment, a correct figure right after a wrong one, a tentative decision before
the final one.

### Vary the surface (so a model can't learn shortcuts)

An independent review of the pilots found the labels sound but the *phrasing* of events too
regular. Across meetings:

- **Near-miss actions** use varied forms: "it'd be good if the deck got another look", "we need
  someone on that", "worth chasing legal", a request to a person who doesn't accept, an "I might
  look at it if I get time" (hedged, no task) — not always "someone should probably …".
- **Unanswered questions** die in different ways: talked over, deflected ("good question, let's
  come back to it"), answered with a non-answer, lost in an interruption, or met with silence and
  a new speaker on the same topic. Not always "Anyway, …".
- **Drifts** start and end without signposts sometimes (a joke that runs on; someone just keeps
  going), and are not always closed by "back to it".
- **Wrong figures** are sometimes corrected late, approximately, by someone unsure, or **never
  corrected at all** — that is exactly where the agent's interjection is worth the most.

The batch-1 audit found a second layer of regularities, so from batch 2 on:

- **Counts vary per meeting.** 0–3 drifts and 0–3 asides, not exactly one of each. Asides are
  not always "Sorry, my X…"; drifts don't always open with "Did anyone…" or run 3–5 turns.
- **About a third of `decision+` lines are implicit**: "Okay, the tent then." / "Tacos it is." —
  no "Decided/Final/Settled/Done" closer. Near-miss decisions don't always start with "Maybe".
- **About a third of `action+` lines are implicit acceptances**: "Fine.", "Then Swedish.",
  "I'd like to." Every request to a named person ("could you…") and every hedged offer gets its
  reply tagged: `action+` if accepted in any words, untagged (with `{~}`) if declined.
- **Wrong figures are clearly wrong** (not a rounding a fact-checker would accept).
- **No recycled material** from this doc or earlier meetings (taco trucks, "Hi, Mango", "You've
  what?", the hidden-promise reveal). Catchphrases are sparse and not tied to tags (a persona
  who always says "bottom line" before a wrong figure teaches the persona, not the content).
- **The last unanswered question is not always just before the closing line.**

After the batch-2 audit (error rate down from ~4.3 to ~1.5 per meeting):

- **Drift openers vary**: no "Speaking of…"; topics are not mostly pets (weather, sport, a
  colleague's news, local politics, a TV show, food), and some asides are short *content*
  asides ("that reminds me of the old office"), not only tech or household interruptions.
- Every `question+` is checked against its next line, and every `@+N` must land on a line that
  answers the specific thing asked (a deferral like "let's hold that" is not an answer).

After the batch-3 audit (0.9 per meeting):

- `{~}` on a `question+` means "checked against the rest of the meeting", not just the next line.
- **Endings vary**: not always "unanswered question, another question, close".
- **Unanswered questions die different ways**, not mostly "the next speaker asks something else".
- **Corrections and excuses vary**: not always "I have the sheet open … it's X, not Y" or
  "I was counting the …"; sometimes the corrector is unsure, or the person just says "oh".
- **No "That reminds me" / "By the way" signposts** on every aside or drift.

After the batch-4 audit (0.75 per meeting):

- `{~}` no longer silences the figure checks. A line that says a number but is not a fact-sheet
  claim (a pickup time, "second author", a derived total) is marked `{~nc}` ("no claim"),
  so a reviewed line can never hide a restated figure again.
- Corrections don't always follow "I checked X … it's Y, not Z"; doubts don't always open with
  "X? I thought Y"; a wrong figure isn't always echoed approvingly by a second speaker.
- Drift content stays off-agenda (no drifts that loop back into the agenda topic), and meetings of
  the same theme don't end the same way.

## Review

Each meeting is self-reviewed against these rules, then `lint()` flags: same speaker twice, a
`claim+` equal to the fact sheet, a question tag without `?`, missing categories, untagged lines
that look like questions/commitments/figures/decisions, **any fact-sheet value (digits, spoken
form or month) said on an untagged line**, and a question inside a drift whose answer falls
outside the span. Lines checked and deliberately left untagged carry `{~}`.

After the batch-1 audit the lint also flags **restatements**: within 4 turns of a line tagged
with fact F#, any untagged line that says F#'s value in any form, including small numbers
("Four, but…"), ordinal dates ("the twenty-fifth"), shorthand ("twelve six" = $12,600,
"three eighty", "zero point six") and times ("half two"); and the **reply to a request** to a
named person, which must be tagged `action+` or marked `{~}`.

The three pilots were also audited line by line by an independent Claude subagent (fresh
context, the rules and Decider's question wording as the rubric). It found ~8 clear errors in
~390 lines, none in planted positives: 5 missed restatements/questions, 2 drift spans that
missed the reply, 2 `@+N` pointers that landed on a non-answer. All were fixed, and the lint
now catches each of those patterns. The same audit is repeated on batches of new meetings.

| Audit | Meetings | Clear errors (missed / wrong / pointer) | Per meeting |
|---|---|---|---|
| Pilots | 3 | 8 | 2.7 |
| Batch 1 | 8 | 34 | 4.3 |
| Batch 2 | 8 | 12 | 1.5 |
| Batch 3 | 8 | 7 | 0.9 |
| Batch 4 | 8 | 6 | 0.75 |

Each audit's findings were applied, and each error class it found was turned into a lint check
where possible: restatements of the right or wrong value within 4 turns, replies to requests,
self-answered questions, `@+N` landing on a question or a deferral, `question+` followed by a
possible answer, mic checks tagged as questions, and short replies just after an aside.

## Grid

8 themes × drama {0.2, 0.5, 0.8} × seed {1, 2} = 48 meetings (the `gen_meetings.py` grid),
~130 turns / ~10 min each, ~25 tagged events per meeting (about 13 positives and 13 hard
negatives, plus answered questions). Split by meeting, stratified by theme (4 dev + 2 test per theme).
Drama sets interruptions, disagreement and how often people misremember figures.

| Theme (`domain_pack`) | Meetings |
|---|---|
| App launch go/no-go (`product_launch`) | 6 (Aurora, Tidewell, Fernhill, Marlowe, Pinecrest, Vantage) |
| Payments team sprint planning (`software_team`) | 6 (Quillpay, Ledgerly, Penny Lane, Kestrel, Brightwater, Tallyho) |
| Checkout outage postmortem (`incident_review`) | 6 (config, cert expiry, migration, fraud API, on-sale, utility portal) |
| Nonprofit gala committee (`nonprofit_events`) | 6 (literacy, rescue, orchestra, land trust, shelter, food bank) |
| School PTA budget (`community_budget`) | 6 (Maplewood, Cedar Hill, Lakeview, Hillcrest, Willow Creek, Oakmont) |
| University ecology lab (`research_lab`) | 6 (Hollis, Calloway, Pine Ridge, wetlands, pollinator, alpine) |
| Community garden committee (`community_group`) | 6 (Elm Street, Fairview, Riverside, Maple Court, Brookside, Eastgate) |
| Family call planning a cousin's wedding (`family_planning`) | 6 (Alvarez, Adeyemi, Kowalski, Nakamura, Osei, Petrov) |

All 48 grid cells (8 themes x drama 0.2/0.5/0.8 x seed 1/2) are written. Built set: 48 meetings,
3,248 windows; dev = 32 meetings / 2,125 windows, test = 16 meetings / 1,123 windows (4 + 2 per theme).

**Known limitation: event density.** About 19% of lines carry a positive event, versus a few
percent in a real meeting (later meetings are shorter, 45-70 turns, than the pilots). Detection
precision/recall are unaffected, but silence-rate and annoyance-per-hour numbers from this set
are pessimistic; padding meetings with neutral talk would bring them closer to real meetings.