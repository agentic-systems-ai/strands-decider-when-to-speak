"""M3 offline eval: run the window questions through Decider (or the Bedrock judge) and score.

    python scripts/eval_decider.py predict --split dev  --backend decider
    python scripts/eval_decider.py predict --split dev  --backend judge --limit 400
    python scripts/eval_decider.py report  --split dev  [--backend decider judge-bedrock]

`predict` writes runs/eval/<backend>_<split>.jsonl (one line per window, resumable); the judge's
file is named after its provider (judge-ollama, judge-bedrock).
`report` prints per-question accuracy / F1 / Brier / hard-negative false-positive rate and
latency, and saves charts to docs/img/: reliability diagrams, coverage-accuracy curves,
a latency histogram.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from interjection_policy import OFF_AGENDA, meeting_questions  # noqa: E402
from when_to_speak.dataset import read_windows  # noqa: E402
from when_to_speak.state import MeetingState  # noqa: E402

RUNS = ROOT / "runs" / "eval"
IMG = ROOT / "docs" / "img"
NOUL_KEYS = ["action_item", "decision_made", "factual_claim", "open_question", "answered_prior"]


def _questions_for(w, packs):
    """The agent's question set for this tick, minus already_flagged (needs runtime state)."""
    st = MeetingState(packs[w.meeting_id])
    qs = meeting_questions(st.agenda_options(), pending_question="answered_prior" in w.labels)
    return [q for q in qs if q.key != "already_flagged"]


def predict(split: str, backend: str, limit: int) -> Path:
    from decider_client import DeciderClient, LLMJudgeClient
    from when_to_speak.dataset import load_meetings

    packs = {m.meeting_id: m.cast.pack for m in load_meetings(ROOT / "data" / "meetings")}
    ws = read_windows(ROOT / "data" / "windows" / f"{split}.jsonl")
    if limit:
        ws = ws[:limit]
    if backend == "judge":
        from when_to_speak.providers import provider
        backend = f"judge-{provider()}"  # one file per provider, so runs don't resume into each other
    out = RUNS / f"{backend}_{split}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        done = {(r["meeting_id"], r["tick"]) for r in map(json.loads, out.read_text().splitlines())}
    client = DeciderClient() if backend == "decider" else LLMJudgeClient()
    if backend == "decider":
        client.warmup()
    with out.open("a", encoding="utf-8") as fh:
        for i, w in enumerate(ws):
            if (w.meeting_id, w.tick) in done:
                continue
            qs = _questions_for(w, packs)
            dec = client.ask(w.state, qs)
            fh.write(json.dumps({
                "meeting_id": w.meeting_id, "tick": w.tick, "labels": w.labels, "hard_neg": w.hard_neg,
                "latency_ms": next(iter(dec.values())).latency_ms, "chars": len(w.state),
                "probs": {k: d.probs for k, d in dec.items()},
            }) + "\n")
            if i % 50 == 0:
                print(f"{i}/{len(ws)}", flush=True)
    if backend.startswith("judge"):
        print("judge usage:", client.usage)
    return out


# ------------------------------------------------------------------ metrics


def _load(backend: str, split: str) -> list[dict]:
    p = RUNS / f"{backend}_{split}.jsonl"
    return [json.loads(line) for line in p.read_text().splitlines()]


def _pairs(rows: list[dict], key: str) -> list[tuple[float, int, bool]]:
    """(P(true), label, is_hard_negative) for a noul key."""
    hard_cat = {"action_item": "action_item", "decision_made": "decision_made",
                "factual_claim": "factual_claim", "open_question": "unanswered_question"}.get(key)
    out = []
    for r in rows:
        if key in r["labels"] and key in r["probs"]:
            out.append((r["probs"][key]["true"], int(bool(r["labels"][key])), hard_cat in r["hard_neg"]))
    return out


def noul_metrics(pairs, t: float = 0.5) -> dict:
    tp = sum(1 for p, y, _ in pairs if p >= t and y)
    fp = sum(1 for p, y, _ in pairs if p >= t and not y)
    fn = sum(1 for p, y, _ in pairs if p < t and y)
    n = len(pairs)
    acc = sum(1 for p, y, _ in pairs if (p >= t) == bool(y)) / n if n else math.nan
    prec = tp / (tp + fp) if tp + fp else math.nan
    rec = tp / (tp + fn) if tp + fn else math.nan
    f1 = 2 * prec * rec / (prec + rec) if prec and rec and not math.isnan(prec + rec) else math.nan
    brier = sum((p - y) ** 2 for p, y, _ in pairs) / n if n else math.nan
    hard = [(p, y) for p, y, h in pairs if h and not y]
    hard_fp = sum(1 for p, _ in hard if p >= t) / len(hard) if hard else math.nan
    return {"n": n, "pos": sum(y for _, y, _ in pairs), "acc": acc, "prec": prec, "rec": rec, "f1": f1,
            "brier": brier, "hard_neg_n": len(hard), "hard_neg_fp": hard_fp}


def choice_metrics(rows: list[dict]) -> dict:
    ys, conf, hits = [], [], []
    for r in rows:
        if "agenda_item" not in r["probs"]:
            continue
        probs = r["probs"]["agenda_item"]
        pred = max(probs, key=probs.get)
        hits.append(pred == r["labels"]["agenda_item"])
        conf.append(probs[pred])
        ys.append(r["labels"]["agenda_item"])
    off = [(r["probs"]["agenda_item"].get(OFF_AGENDA, 0.0), int(r["labels"]["agenda_item"] == OFF_AGENDA), False)
           for r in rows if "agenda_item" in r["probs"]]
    return {"n": len(hits), "acc": sum(hits) / len(hits) if hits else math.nan, "off_agenda": noul_metrics(off)}


def report(split: str, backends: list[str]) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    IMG.mkdir(parents=True, exist_ok=True)
    data = {b: _load(b, split) for b in backends if (RUNS / f"{b}_{split}.jsonl").exists()}
    for b, rows in data.items():
        lat = sorted(r["latency_ms"] for r in rows)
        print(f"\n== {b} on {split}: {len(rows)} windows; latency p50 {lat[len(lat) // 2]:.0f} ms, "
              f"p95 {lat[int(0.95 * (len(lat) - 1))]:.0f} ms (all questions in one call)")
        print(f"  {'question':16s} {'n':>5s} {'pos':>4s} {'acc':>6s} {'prec':>6s} {'rec':>6s} {'f1':>6s} "
              f"{'brier':>6s} {'hardFP':>7s}")
        for k in NOUL_KEYS:
            m = noul_metrics(_pairs(rows, k))
            print(f"  {k:16s} {m['n']:5d} {m['pos']:4d} {m['acc']:6.3f} {m['prec']:6.3f} {m['rec']:6.3f} "
                  f"{m['f1']:6.3f} {m['brier']:6.3f} {m['hard_neg_fp']:7.3f} (of {m['hard_neg_n']})")
        c = choice_metrics(rows)
        o = c["off_agenda"]
        print(f"  {'agenda_item':16s} {c['n']:5d}      {c['acc']:6.3f}   off_agenda: prec {o['prec']:.3f} "
              f"rec {o['rec']:.3f} brier {o['brier']:.3f}")

    # Reliability diagrams + coverage-accuracy, one panel per noul question.
    for kind in ("reliability", "coverage"):
        fig, axes = plt.subplots(1, len(NOUL_KEYS), figsize=(4 * len(NOUL_KEYS), 4), squeeze=False)
        for ax, k in zip(axes[0], NOUL_KEYS):
            for b, rows in data.items():
                pairs = _pairs(rows, k)
                if not pairs:
                    continue
                if kind == "reliability":
                    xs, ys = [], []
                    for lo in [i / 10 for i in range(10)]:
                        bucket = [(p, y) for p, y, _ in pairs if lo <= p < lo + 0.1 or (lo == 0.9 and p == 1.0)]
                        if bucket:
                            xs.append(sum(p for p, _ in bucket) / len(bucket))
                            ys.append(sum(y for _, y in bucket) / len(bucket))
                    ax.plot(xs, ys, "o-", label=b)
                    ax.plot([0, 1], [0, 1], ":", color="gray")
                    ax.set_xlabel("predicted P(true)")
                    ax.set_ylabel("observed frequency")
                else:
                    # Act only when max(p, 1-p) >= t: coverage vs accuracy as t rises.
                    cov, acc = [], []
                    for t in [0.5 + i * 0.025 for i in range(20)]:
                        kept = [(p, y) for p, y, _ in pairs if max(p, 1 - p) >= t]
                        if kept:
                            cov.append(len(kept) / len(pairs))
                            acc.append(sum((p >= 0.5) == bool(y) for p, y in kept) / len(kept))
                    ax.plot(cov, acc, "o-", ms=3, label=b)
                    ax.set_xlabel("coverage")
                    ax.set_ylabel("accuracy")
            ax.set_title(k)
            ax.legend()
        fig.tight_layout()
        fig.savefig(IMG / f"{kind}_{split}.png", dpi=120)
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    for b, rows in data.items():
        ax.hist([r["latency_ms"] for r in rows], bins=40, alpha=0.6, label=b)
    ax.set_xlabel("ms per window (all questions)")
    ax.set_xscale("log")
    ax.legend()
    fig.tight_layout()
    fig.savefig(IMG / f"latency_{split}.png", dpi=120)
    print(f"\ncharts -> {IMG}")


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("predict")
    p.add_argument("--split", default="dev")
    p.add_argument("--backend", choices=["decider", "judge"], default="decider")
    p.add_argument("--limit", type=int, default=0)
    r = sub.add_parser("report")
    r.add_argument("--split", default="dev")
    r.add_argument("--backend", nargs="+", default=["decider", "judge-ollama", "judge-bedrock"])
    args = ap.parse_args()
    if args.cmd == "predict":
        print(predict(args.split, args.backend, args.limit))
    else:
        report(args.split, args.backend)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
