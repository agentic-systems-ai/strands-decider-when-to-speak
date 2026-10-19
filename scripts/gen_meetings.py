"""Generate simulated meetings (M1/M2).

    python scripts/gen_meetings.py --pilot            # 3 meetings to read and tune prompts on
    python scripts/gen_meetings.py --grid --workers 6 # 8 themes x 3 drama x 2 seeds = 48

Outputs data/meetings/<meeting_id>/meeting.json, then data/windows/{dev,test}.jsonl split
by meeting (60/40). All LLM responses are cached, so reruns are free.
"""

from __future__ import annotations

import argparse
import random
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from when_to_speak.dataset import load_meetings, write_windows  # noqa: E402
from when_to_speak.llm import LLM  # noqa: E402
from when_to_speak.simulator import SimConfig, simulate  # noqa: E402

THEMES = [
    ("Go/no-go for the Aurora mobile app launch", "product_launch"),
    ("Sprint planning for a payments team at a fictional fintech", "software_team"),
    ("Incident postmortem: the checkout outage last Tuesday", "incident_review"),
    ("Planning committee for a nonprofit's annual fundraising gala", "nonprofit_events"),
    ("School PTA budget meeting for next year", "community_budget"),
    ("Weekly meeting of a university ecology research lab", "research_lab"),
    ("Community garden committee: plots, water and the spring fair", "community_group"),
    ("Family video call planning a cousin's wedding", "family_planning"),
]
DRAMA = [0.2, 0.5, 0.8]
SEEDS = [1, 2]


def grid() -> list[SimConfig]:
    return [SimConfig(theme=t, domain_pack=d, drama=dr, seed=s, duration_min=20, participants=4)
            for t, d in THEMES for dr in DRAMA for s in SEEDS]


def pilot() -> list[SimConfig]:
    return [SimConfig(theme=THEMES[0][0], domain_pack=THEMES[0][1], drama=0.6, seed=1),
            SimConfig(theme=THEMES[7][0], domain_pack=THEMES[7][1], drama=0.8, seed=1),
            SimConfig(theme=THEMES[2][0], domain_pack=THEMES[2][1], drama=0.3, seed=1)]


def split(meeting_ids: list[str], seed: int = 13) -> tuple[set[str], set[str]]:
    ids = sorted(meeting_ids)
    random.Random(seed).shuffle(ids)
    k = round(len(ids) * 0.6)
    return set(ids[:k]), set(ids[k:])


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--pilot", action="store_true")
    g.add_argument("--grid", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "meetings")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    cfgs = pilot() if args.pilot else grid()
    if args.limit:
        cfgs = cfgs[: args.limit]
    llm = LLM()
    print(f"model {llm.model_id}; {len(cfgs)} meetings; {args.workers} workers")
    failed = []
    with ThreadPoolExecutor(args.workers) as ex:
        futs = {ex.submit(simulate, c, llm, args.out): c for c in cfgs}
        for f in as_completed(futs):
            try:
                f.result()
            except Exception as e:  # keep going; report at the end
                failed.append((futs[f].meeting_id, repr(e)))
                print(f"FAILED {futs[f].meeting_id}: {e!r}")
    print("usage:", llm.usage)

    meetings = load_meetings(args.out)
    dev, test = split([m.meeting_id for m in meetings])
    wdir = ROOT / "data" / "windows"
    n_dev = write_windows([m for m in meetings if m.meeting_id in dev], wdir / "dev.jsonl")
    n_test = write_windows([m for m in meetings if m.meeting_id in test], wdir / "test.jsonl")
    print(f"windows: dev={n_dev} ({len(dev)} meetings)  test={n_test} ({len(test)} meetings)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
