"""Pick per-category speak/note thresholds from labelled windows (dev split only).

    python scripts/tune_thresholds.py --labels runs/eval/decider_dev.jsonl --target-precision 0.9

Input: JSONL, one window per line, with
    {"probs": {"<category>": {"true": p, "false": 1-p}} or {"<category>": p},
     "labels": {"<category>": true|false}}
(the output of scripts/eval_decider.py predict has this shape; so can your own data).

speak = the lowest threshold whose precision on these windows is >= --target-precision
        (an interjection should almost always be justified)
note  = the highest threshold whose recall is >= --target-recall
        (silent notes are cheap; catch most events for the recap)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _p(v) -> float:
    return float(v["true"]) if isinstance(v, dict) else float(v)


def sweep(pairs: list[tuple[float, bool]]) -> list[tuple[float, float, float, int]]:
    """(threshold, precision, recall, n_fired) for thresholds 0.05..0.99."""
    pos = sum(y for _, y in pairs)
    out = []
    for i in range(5, 100):
        t = i / 100
        fired = [(p, y) for p, y in pairs if p >= t]
        tp = sum(y for _, y in fired)
        prec = tp / len(fired) if fired else 1.0
        rec = tp / pos if pos else 1.0
        out.append((t, prec, rec, len(fired)))
    return out


def tune(pairs, target_precision: float, target_recall: float) -> tuple[float, float]:
    rows = sweep(pairs)
    speak = next((t for t, prec, _, n in rows if prec >= target_precision and n > 0), 0.99)
    note = max((t for t, _, rec, _ in rows if rec >= target_recall), default=0.05)
    return speak, min(note, speak)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", type=Path, required=True)
    ap.add_argument("--target-precision", type=float, default=0.9)
    ap.add_argument("--target-recall", type=float, default=0.9)
    ap.add_argument("--keys", nargs="*", default=None)
    args = ap.parse_args()

    rows = [json.loads(line) for line in args.labels.read_text(encoding="utf-8").splitlines() if line.strip()]
    keys = args.keys or sorted({k for r in rows for k, v in r["labels"].items() if isinstance(v, bool)})
    result = {}
    print(f"{'category':16s} {'n':>5s} {'pos':>4s} {'speak':>6s} {'prec@speak':>10s} {'rec@speak':>9s} {'note':>6s}")
    for k in keys:
        pairs = [(_p(r["probs"][k]), bool(r["labels"][k])) for r in rows
                 if k in r["labels"] and k in r["probs"] and isinstance(r["labels"][k], bool)]
        if not pairs:
            continue
        speak, note = tune(pairs, args.target_precision, args.target_recall)
        _, prec, rec, _ = next(x for x in sweep(pairs) if abs(x[0] - speak) < 1e-9)
        result[k] = {"speak": speak, "note": note}
        print(f"{k:16s} {len(pairs):5d} {sum(y for _, y in pairs):4d} {speak:6.2f} {prec:10.3f} {rec:9.3f} {note:6.2f}")
    print("\n" + json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
