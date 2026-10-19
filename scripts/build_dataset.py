"""Build the prebuilt dataset from authored meetings (data/authored/*.md).

    python scripts/build_dataset.py            # parse, lint, write meetings + windows
    python scripts/build_dataset.py --check    # parse and lint only

Writes data/meetings/<meeting_id>/meeting.json and data/windows/{dev,test}.jsonl. The split
is by meeting, stratified by domain pack (about 60/40), so every theme appears in both.
"""

from __future__ import annotations

import argparse
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from when_to_speak.authored import AuthoringError, build, lint  # noqa: E402
from when_to_speak.dataset import windows, write_windows  # noqa: E402
from when_to_speak.schema import Meeting  # noqa: E402


def split(meetings: list[Meeting], seed: int = 13, dev_frac: float = 0.6) -> tuple[set[str], set[str]]:
    by_pack: dict[str, list[str]] = defaultdict(list)
    for m in meetings:
        by_pack[m.config.get("domain_pack", "")].append(m.meeting_id)
    dev: set[str] = set()
    test: set[str] = set()
    rng = random.Random(seed)
    for pack in sorted(by_pack):
        ids = sorted(by_pack[pack])
        rng.shuffle(ids)
        k = max(1, round(len(ids) * dev_frac)) if len(ids) > 1 else 1
        dev.update(ids[:k])
        test.update(ids[k:])
    return dev, test


def summary(m: Meeting) -> str:
    c = Counter((g.category, g.polarity) for g in m.gold)
    cats = " ".join(f"{k.split('_')[0][:6]}{c[(k, 'pos')]}/{c[(k, 'neg')]}"
                    for k in ("action_item", "decision_made", "factual_claim", "unanswered_question",
                              "off_topic_drift"))
    return (f"{m.meeting_id:44s} {len(m.turns):4d} turns {m.timeline[-1].end_s / 60:5.1f} min  "
            f"pos/neg: {cats}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, default=ROOT / "data" / "authored")
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "meetings")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    meetings: list[Meeting] = []
    errors = 0
    for p in sorted(args.src.glob("*.md")):
        try:
            m = build(p.read_text(encoding="utf-8"), source_name=p.name)
        except (AuthoringError, KeyError, ValueError) as e:
            print(f"ERROR {p.name}: {e}")
            errors += 1
            continue
        meetings.append(m)
        print(summary(m))
        for w in lint(m):
            print(f"    warn: {w}")
    if errors or args.check:
        return 1 if errors else 0

    ids = [m.meeting_id for m in meetings]
    if len(ids) != len(set(ids)):
        print("ERROR: duplicate meeting_id")
        return 1
    for m in meetings:
        d = args.out / m.meeting_id
        d.mkdir(parents=True, exist_ok=True)
        (d / "meeting.json").write_text(m.model_dump_json(indent=1), encoding="utf-8", newline="\n")

    dev, test = split(meetings)
    wdir = ROOT / "data" / "windows"
    n_dev = write_windows([m for m in meetings if m.meeting_id in dev], wdir / "dev.jsonl")
    n_test = write_windows([m for m in meetings if m.meeting_id in test], wdir / "test.jsonl")
    (wdir / "split.txt").write_text("".join(f"{'dev ' if i in dev else 'test'} {i}\n" for i in sorted(ids)),
                                    encoding="utf-8", newline="\n")

    labels = Counter()
    for m in meetings:
        for w in windows(m):
            for k, v in w.labels.items():
                if v is True or (k == "agenda_item" and v == "off_agenda"):
                    labels[k] += 1
    print(f"\n{len(meetings)} meetings; windows dev={n_dev} ({len(dev)} meetings) "
          f"test={n_test} ({len(test)} meetings)")
    print("positive windows:", dict(labels))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
