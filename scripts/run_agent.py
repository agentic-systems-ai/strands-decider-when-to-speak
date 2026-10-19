"""Headless mode-A run of the meeting agent over simulated meetings, with an event-level report.

    python scripts/run_agent.py --split test            # all test meetings
    python scripts/run_agent.py --meeting <meeting_id>  # one meeting

Needs the Decider server (DECIDER_URL) and Bedrock (BEDROCK_MODEL_MAIN).
Writes runs/agent/<meeting_id>/{ticks.jsonl,score.json,recap.json} and prints a summary.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from decider_client import DeciderClient  # noqa: E402

from when_to_speak.agent import MeetingAgent  # noqa: E402
from when_to_speak.dataset import load_meetings  # noqa: E402
from when_to_speak.replay import utterances  # noqa: E402
from when_to_speak.schema import CATEGORIES  # noqa: E402
from when_to_speak.scoring import score_meeting  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["dev", "test", "all"], default="test")
    ap.add_argument("--meeting", action="append", default=[])
    ap.add_argument("--meetings-dir", type=Path, default=ROOT / "data" / "meetings")
    ap.add_argument("--out", type=Path, default=ROOT / "runs" / "agent")
    ap.add_argument("--no-recap", action="store_true")
    ap.add_argument("--ungated", action="store_true", help="baseline: no Decider, the LLM sees every line")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # model text can hold any Unicode; Windows consoles default to cp1252

    meetings = load_meetings(args.meetings_dir)
    if args.meeting:
        meetings = [m for m in meetings if m.meeting_id in args.meeting]
    elif args.split != "all":
        ids = {json.loads(line)["meeting_id"]
               for line in (ROOT / "data" / "windows" / f"{args.split}.jsonl").read_text().splitlines()}
        meetings = [m for m in meetings if m.meeting_id in ids]

    decider = None
    if not args.ungated:
        decider = DeciderClient()
        decider.warmup()
    totals = {c: [0, 0, 0] for c in CATEGORIES}
    agg = {"minutes": 0.0, "ticks": 0, "wakes": 0, "spoken": 0, "unjustified": 0, "in": 0, "out": 0}
    for m in meetings:
        agent = MeetingAgent(m.cast.pack, decider, gated=not args.ungated)
        for u in utterances(m):
            tr = agent.on_utterance(u)
            if tr.spoken:
                print(f"  {tr.t:7.1f}s  AGENT ({tr.category} {tr.confidence:.2f}): {tr.spoken}")
        s = score_meeting(m, agent.ticks)
        d = args.out / m.meeting_id
        d.mkdir(parents=True, exist_ok=True)
        (d / "ticks.jsonl").write_text("\n".join(t.model_dump_json() for t in agent.ticks), encoding="utf-8")
        (d / "score.json").write_text(s.model_dump_json(indent=1), encoding="utf-8")
        if not args.no_recap:
            try:  # the recap is not scored; a bad reply should not stop the run
                (d / "recap.json").write_text(agent.recap().model_dump_json(indent=1), encoding="utf-8")
            except ValueError as e:
                print(f"  recap failed: {str(e).splitlines()[0]}")
        print(f"{m.meeting_id}: {s.ticks} ticks, LLM skipped {s.llm_skip_rate:.1%}, spoken {s.spoken} "
              f"({s.unjustified_spoken} unjustified), annoyance {s.annoyance_per_hour:.1f}/h")
        for c, cs in s.per_category.items():
            totals[c][0] += cs.tp
            totals[c][1] += cs.fp
            totals[c][2] += cs.fn
        agg["minutes"] += s.minutes
        agg["ticks"] += s.ticks
        agg["wakes"] += s.wakes
        agg["spoken"] += s.spoken
        agg["unjustified"] += s.unjustified_spoken
        agg["in"] += agent.llm_usage["input_tokens"]
        agg["out"] += agent.llm_usage["output_tokens"]

    print("\ncategory              precision  recall   (tp/fp/fn)")
    for c, (tp, fp, fn) in totals.items():
        p = tp / (tp + fp) if tp + fp else float("nan")
        r = tp / (tp + fn) if tp + fn else float("nan")
        print(f"  {c:20s} {p:8.2f} {r:8.2f}   ({tp}/{fp}/{fn})")
    hours = agg["minutes"] / 60 or 1
    print(f"\nLLM calls avoided: {1 - agg['wakes'] / max(1, agg['ticks']):.1%} of {agg['ticks']} ticks")
    print(f"annoyance: {agg['unjustified'] / hours:.1f} unjustified spoken/hour; "
          f"spoken {agg['spoken'] / hours:.1f}/hour; LLM tokens in={agg['in']} out={agg['out']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
