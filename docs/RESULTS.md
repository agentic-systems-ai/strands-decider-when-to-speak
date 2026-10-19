# Results

What we measured, how, and what it does and doesn't show. All numbers come from the
committed dataset (48 authored meetings: dev 2,125 windows, test 16 meetings / 1,123 lines /
86 minutes) and can be reproduced with the commands at the end.

**The short version.** A 2B Decider running locally answers "did anything just happen?" in
about 370 ms with a flat latency tail, and it doesn't fall for planted near-misses. A
general-purpose LLM asked the same questions detects more, but it is slower, has a long tail,
and costs tokens on every line. Put in front of an LLM agent, the Decider skips about three
lines in four. That cuts input tokens 4× and unjustified interruptions 3.4× compared with
letting the LLM see everything.

> **Model note.** The LLM in these runs is `gpt-oss-20b` on Amazon Bedrock, chosen to keep
> the project's cost to a few dollars. Claude Haiku 5.5 was not enabled on our accounts at the
> time. A cheap model makes the token savings look small in dollars; at Claude Sonnet 5.5 or
> Opus 5.5 prices the same token counts cost about 30× or 60× more (see [Tokenomics](#tokenomics)).

## 1. Detection: Decider vs an LLM judge (dev, per window)

Each of the 2,125 dev windows is the agent's rolling meeting state at one line. Both backends
answer the same typed questions in one call per window. The judge is the same prompt sent to
an LLM with a forced JSON answer.

| Question | Decider 2B (local) | gpt-oss-20b judge (Bedrock) | qwen3:8b judge (local, 600 windows) |
|---|---|---|---|
| Action item (F1) | 0.37 | **0.56** | 0.18 |
| Decision made (F1) | 0.30 | **0.47** | 0.25 |
| Figure claim (F1) | 0.66 | **0.79** | 0.60 |
| Open question (F1) | 0.41 | **0.84** | 0.65 |
| Pending question answered (F1) | 0.54 | **0.69** | 0.58 |
| Fell for action-item traps | **0%** of 44 | 18% | 100% of 14 |
| Fell for decision traps | **3%** of 68 | 9% | 33% of 18 |
| Latency p50 / p95 | **366 / 433 ms** | 1,201 / 5,729 ms | 2,564 / 3,212 ms |
| Cost | local GPU (RTX 3060) | ~$0.0001 per window | local GPU |

Traps are planted near-misses: "someone should probably look at that" (not a commitment),
"let's lean towards June" (not a decision).

What this shows:

- **A capable LLM detects better.** We don't claim otherwise. `gpt-oss-20b` beats the Decider
  on every question's F1.
- **The Decider is fast and steady.** Its p95 is within 70 ms of its p50, so it can run on
  every line of a live conversation. The Bedrock judge's p95 is 5.7 s: queueing and reasoning
  time you don't control.
- **The Decider doesn't take the bait.** It flagged 0 of 44 action-item traps, and the LLM
  judges flagged 18% to 100%. For an agent that speaks out loud, a false "I'll note that as
  your action item" costs more than a miss.
- **It runs locally and offline.** It has no API dependency, no noisy neighbours and no
  per-call cost.

Charts: [`img/coverage_dev.png`](img/coverage_dev.png),
[`img/latency_dev.png`](img/latency_dev.png), [`img/reliability_dev.png`](img/reliability_dev.png).

### Decider latency by hardware

The same 2,125 dev windows through the same Decider server, one call per window (all questions
batched):

| Where | p50 | p95 | p99 | Notes |
|---|---|---|---|---|
| AWS g6.xlarge, NVIDIA L4 (us-east-2) | **163 ms** | **184 ms** | 189 ms | Deployed with `infra/`; Linux fast kernels (`flash-linear-attention`); max 783 ms |
| Laptop, RTX 3060 12 GB (Windows) | 366 ms | 433 ms | | No fast kernels on Windows |
| AWS g6.xlarge host CPU only, 4 vCPU (AMD EPYC 7R13) | ~15 s | | | Rate-timed: 4 calls a minute, then stopped; CPU-only PyTorch |

Per-question precision, recall and F1 on the L4 matched the laptop run to within 0.01, so the
deployment answers the way the local server does. On CPU the Decider is about 90× slower than
on the L4. A meeting produces a line every few seconds, so it needs a GPU.

The deployed app replaying the 136-line Aurora meeting end to end: Decider 154 / 170 ms p50 /
p95 per line. 83% of lines skipped the LLM. `gpt-oss-20b`, called from the same region, took
448 / 996 ms per woken line. The first Decider call on a fresh host took 14 s, most likely
Triton compiling kernels.

### Tuning that came out of the dev eval

Three changes, each measured on dev before touching test:

| Change | Before | After |
|---|---|---|
| Ask "is this an off-topic tangent?" as its own yes/no question, instead of an `off_agenda` option in the agenda choice | recall 0.02 | recall 0.66, precision 0.84 at p ≥ 0.7 ¹ |
| Count a pending question as answered from p ≥ 0.3 (the Decider is under-confident here) | F1 0.54 | F1 0.83 |
| Start a pending question only on a line with "?" | precision 0.36 | precision 0.93, same recall |

¹ Measured on all 116 off-topic windows plus 500 sampled others, about 4× the real
off-topic share, so precision in a real meeting is lower. The agent also requires three
off-topic lines in a row.

## 2. The agent: with and without the Decider (test, per event)

The same Strands agent ran over the 16 test meetings twice, with the same tools, prompt
categories, 60 s speech cooldown and 4 model calls per wake. In the gated run, the Decider
decides which lines wake the LLM. In the ungated run, every line wakes it, and the LLM decides
for itself whether a category applies. Events are scored against the planted labels.

| | Gated (Decider → gpt-oss-20b) | Ungated (gpt-oss-20b on every line) |
|---|---|---|
| Lines that reached the LLM | **305 of 1,123 (27%)** | 1,123 (100%) |
| LLM input / output tokens | **0.58M / 26k** | 2.31M / 87k |
| Unjustified spoken lines per meeting-hour | **7.7** | 25.8 |
| All spoken lines per meeting-hour | 37.7 | 70.5 |
| Action items (precision / recall) | **0.64** / 0.43 | 0.39 / **0.83** |
| Decisions | 0.39 / **0.61** | **0.52** / 0.24 |
| Wrong figures corrected out loud | 0.86 / 0.51 | **0.89 / 0.81** |
| Unanswered questions nudged | 0.18 / 0.21 | 0.16 / 0.12 |
| Off-topic drift nudged | **0.22 / 0.35** | 0.00 / 0.00 |
| LLM latency per woken line, p50 / p95 | 0.9 / 7.4 s | 1.0 / 6.8 s |

The test meetings are scripted and dense: about 13 lines a minute, with planted events
throughout. That's why both runs speak more per hour than a real meeting would need.

What this shows:

- **The agent speaks less and interrupts wrongly 3.4× less often.** An LLM that sees every
  line finds something to say on most of them.
- **It's a trade, not a free win.** The ungated LLM catches more action items and wrong
  figures, because it looks at every line. The gated agent catches more decisions and is the
  only one that catches off-topic drift. That drift question is the Decider's.
- **Some things are hard for both.** Nudging an unanswered question works poorly either way.
  Deciding that a question was left hanging, as opposed to answered three lines later or
  dropped on purpose, is still open.

### Tokenomics

The same token counts, priced at Bedrock on-demand list prices in us-east-2 (input / output per
million tokens, global cross-region inference; in-region inference is 10% more), from the AWS
Pricing API in October 2026. We paid only the `gpt-oss-20b` row; the others are what the same
tokens would cost.

| Model | Gated | Ungated | Per meeting-hour, gated vs ungated |
|---|---|---|---|
| gpt-oss-20b ($0.07 / $0.30) | $0.05 | $0.19 | $0.03 vs $0.13 |
| Claude Haiku 5.5 ($0.10 / $0.50) | $0.07 | $0.27 | $0.05 vs $0.19 |
| Claude Sonnet 5.5 ($2 / $10) | $1.41 | $5.49 | $0.99 vs $3.84 |
| Claude Opus 5.5 ($4 / $20) | $2.83 | $10.99 | $1.98 vs $7.68 |

Our per-call prompt is small, about 1–2k tokens: the rolling window, the fact sheet and the
tool schemas. An agent that carries the whole transcript, documents or memory pays per
line in proportion to that context. The Decider's fixed cost is a local 2B forward pass.

"Use the cheapest model that is good enough" is a fair alternative, and `gpt-oss-20b` is
cheap. But a cheap model still adds 1–7 s of latency and an outside dependency to every line,
and it still talks too much when it sees everything.

## Caveats

- **Scripted meetings.** The meetings are authored with planted events, independently audited
  ([DATA.md](DATA.md)). They are not recordings of real meetings.
- **Single runs.** Agent results are single runs, and LLM output varies. Two gated runs with
  identical fact-check logic gave figure-correction recall of 0.63 and 0.51. Differences of a
  few points are noise.
- **gpt-oss quirks.** `gpt-oss-20b` sometimes returned a malformed tool name, an empty reply or
  a bare `"true"`. The code tolerates these (see git history). 28 of 2,125 judge answers (1.3%)
  were unusable and scored as 50/50.
- **Token counts before commit 99ad93f are wrong.** An accounting bug summed Strands' running
  total on every call. All numbers here come from runs after the fix.

## Reproduce

```bash
.venv/Scripts/strands-decider serve StrandsAgents/strands-decider-2B-qwen3.5-v1-2610 --port 8099 --device cuda
python scripts/eval_decider.py predict --split dev --backend decider
LLM_PROVIDER=bedrock AWS_REGION=us-east-2 BEDROCK_MODEL_BASELINE=openai.gpt-oss-20b-1:0 \
  python scripts/eval_decider.py predict --split dev --backend judge
python scripts/eval_decider.py report --split dev

export LLM_PROVIDER=bedrock AWS_REGION=us-east-2 BEDROCK_MODEL_MAIN=openai.gpt-oss-20b-1:0
python scripts/run_agent.py --split test --no-recap --out runs/agent-gated
python scripts/run_agent.py --split test --no-recap --ungated --out runs/agent-ungated
```
