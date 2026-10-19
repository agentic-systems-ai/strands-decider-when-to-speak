# Pattern: `interjection_policy`

> **Should my agent speak now, and why?** A reusable Strands Decider pattern for any agent
> that watches a stream: meetings, Slack channels, support chats, logs, game commentary.

An LLM that reads every chunk of a stream is slow, expensive, and falls behind. This
pattern puts a 2B decision model in front of it. For each new chunk, Strands Decider
answers a few yes/no questions about the latest lines (one batched forward pass,
about 370 ms p50 / 430 ms p95 on an RTX 3060). A plain-Python policy turns those calibrated probabilities
into one of three behaviours:

| Tier | When | What happens | LLM tokens |
|---|---|---|---|
| `SPEAK` | `p >= speak` | the agent is woken, told *which* category fired and how confident the gate is | yes |
| `NOTE` | `note <= p < speak` | a silent margin card for the UI or recap | none |
| `SILENT` | `p < note` | nothing | none |

Guards: a **cooldown** (at most one spoken interjection per N seconds; extra SPEAKs become
NOTEs), **dedupe** (suppress if the point repeats something already flagged), and a
**streak** requirement (for example, "off-agenda for 3 ticks in a row").

## Install

```bash
pip install -e ".[decider]"   # from this repo; or copy patterns/interjection_policy/ + decider_client.py
strands-decider serve StrandsAgents/strands-decider-2B-qwen3.5-v1-2610 --port 8099 --device cuda
```

## Use it (5 lines)

```python
gate = InterjectionGate(DeciderClient(),
                        make_interjection_questions({"bug_report": "a report of a software bug or outage"}),
                        TieredPolicy({"bug_report": Thresholds(speak=0.8, note=0.5)}))
agent = Agent(model=..., interventions=[InterjectionIntervention(gate, render_state=lambda _: window.render())])
agent(new_chunk)   # Deny'd with no LLM call unless the gate says SPEAK
```

Without Strands, call `gate.should_wake(state)` and branch on `result.action`.
[`example.py`](example.py) is a 30-line Slack lurker.

## What it decides

One **noul** (yes/no) question per category, all against the same state:

```
AGENDA ITEM (current): launch_date - Pick the public launch date
ALREADY FLAGGED: (none)
RECENT TRANSCRIPT (oldest->newest):
[Dana] Okay so legal still hasn't seen the new deck.
[Raj] Yeah, they flagged the privacy section last time.
>> LATEST: [Mei] I'll send the revised deck to legal by Thursday.
```

Built-in meeting categories (`MEETING_CATEGORIES`):

| key | question | true | false |
|---|---|---|---|
| `action_item` | Did someone in the LATEST lines commit to doing a specific task? | a person committed to a concrete task (owner + action) | no commitment, or only a vague suggestion |
| `decision_made` | Did the group reach a final decision in the LATEST lines? | an explicit, settled decision | options discussed, tentative, or undecided |
| `factual_claim` | Do the LATEST lines state a specific number, date or metric that could be checked against the fact sheet? | a specific checkable figure | none |
| `open_question` | Do the LATEST lines ask a question directed at the group that still needs an answer? | a real, unanswered question | none, rhetorical, or answered at once |
| `answered_prior` | Has the PENDING question been answered? | answered or assigned | still open |
| `off_agenda` (`OFF_TOPIC`, opt-in) | Are the LATEST lines an off-topic tangent rather than meeting business? | chit-chat, news, jokes, personal matters | meeting business |
| `agenda_item` (choice, optional) | Which agenda item is being discussed? | each agenda item + `off_agenda` | |
| `already_flagged` | Is the LATEST point the same as something in ALREADY FLAGGED? | repeat | new |

Ask about drift with `meeting_questions(off_topic=True)` rather than the agenda choice: on our
dev set the Decider almost never picked `off_agenda` as a choice option (recall 0.02), but
answered the direct yes/no question well (recall 0.66 at p ≥ 0.7).

Why several nouls instead of one big choice: events co-occur ("Okay, June 3rd, and I'll
tell marketing" is both a decision and an action item), and each noul gets its own
calibrated probability.

## Defining your own categories

```python
make_interjection_questions({
    "bug_report": "a report of a software bug or outage",          # short form
    "pricing_q": Category(                                          # full form
        question="Does the LATEST message ask about pricing or plans?",
        true="the user asks what something costs or which plan to buy",
        false="pricing is not asked about, or only mentioned in passing"),
})
```

Wording tips (decision models are sensitive to wording, so track versions):
- Ask about the **LATEST** lines only. Local questions are what a 2B model is good at.
- Put the hard negative in the `false` description ("only a vague suggestion").
- One judgement per question. Split "is it a bug *and* urgent?" into two.

## Tuning thresholds

Thresholds are config. Label about 100 windows from your own stream (true/false per
category), run them through the gate, and choose `speak` as the lowest threshold whose
precision on your dev split meets your annoyance budget, and `note` for the recall you
want in the recap:

```bash
python scripts/tune_thresholds.py --labels my_windows.jsonl --target-precision 0.9
```

The cooldown is a product decision: 60 s suits a meeting; for a busy Slack channel,
consider per-thread cooldowns.

## When NOT to use this

- **Every chunk needs a response** (a chatbot). There is nothing to gate.
- **The judgement needs long context**: "did we already discuss this 40 minutes ago?"
  The gate sees a ~700-token window. Keep long-range memory in the agent.
- **Sarcasm and irony.** "Oh great, *another* outage, love that for us" can read either
  way. Expect lower confidence, which the NOTE tier absorbs.
- **Long monologues.** The window keeps the tail of an over-long line; a commitment
  buried in the middle of a 2-minute speech may be missed. Tick every few seconds
  during long turns (the meeting agent does this).
- **Hard, unfamiliar rubrics.** Decider is near-perfect on easy, local judgements and
  much weaker on multi-step reasoning. If your category needs reasoning, let the gate
  detect the *candidate* and let the LLM do the reasoning (the meeting agent's
  fact-check works this way).

## Files

| File | What |
|---|---|
| `questions.py` | `make_interjection_questions`, meeting defaults, agenda choice builder |
| `policy.py` | `TieredPolicy` (tiers, cooldown, dedupe, streak), `signals_from` |
| `window.py` | `RollingWindow`: token-budgeted window with the `>> LATEST:` marker |
| `strands_wiring.py` | `InterjectionGate` (framework-free) and `InterjectionIntervention` (Strands) |
| `example.py` | Slack lurker |
| `test_pattern.py` | unit tests (no GPU, no AWS) |
