"""M0: run the 7 meeting questions on hand-written windows and eyeball the answers.

    python scripts/m0_smoke.py [--url http://127.0.0.1:8099] [--repeat 5]

Each window has the answers we expect; the script prints Decider's P(true) next to
them, flags disagreements, and reports latency (warm-up excluded).
"""

from __future__ import annotations

import argparse
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from decider_client import DeciderClient  # noqa: E402

from interjection_policy import RollingWindow, meeting_questions  # noqa: E402

AGENDA = [
    ("launch_date", "Pick the public launch date for the Aurora app"),
    ("crash_metrics", "Review crash-free sessions and stability before launch"),
    ("store_assets", "App store screenshots, copy and listing"),
]
FACT_KEYS = "crash_free_sessions_last_week, launch_date_candidate, beta_testers, marketing_budget"

# (name, lines, current agenda item, pending question, already flagged, expected)
WINDOWS = [
    ("action_item+", [
        ("Dana", "Okay so legal still hasn't seen the new deck."),
        ("Raj", "Yeah, they flagged the privacy section last time."),
        ("Mei", "I'll send the revised deck to legal by Thursday."),
    ], "store_assets", None, [],
     {"action_item": 1, "decision_made": 0, "factual_claim": 0, "open_question": 0,
      "agenda_item": "store_assets", "already_flagged": 0}),
    ("action_item- (vague)", [
        ("Dana", "Okay so legal still hasn't seen the new deck."),
        ("Raj", "Yeah, they flagged the privacy section last time."),
        ("Mei", "Someone should probably look at the deck at some point, I guess."),
    ], "store_assets", None, [],
     {"action_item": 0, "decision_made": 0, "factual_claim": 0, "open_question": 0,
      "agenda_item": "store_assets", "already_flagged": 0}),
    ("decision+ & claim", [
        ("Raj", "We've gone back and forth on this for three weeks."),
        ("Dana", "Crash-free is like 97% right now, which is fine for launch."),
        ("Mei", "Okay, we're going with June 3rd. That's final."),
    ], "launch_date", None, [],
     {"action_item": 0, "decision_made": 1, "factual_claim": 0, "open_question": 0,
      "agenda_item": "launch_date", "already_flagged": 0}),
    ("claim+", [
        ("Mei", "Before we pick a date, where are we on stability?"),
        ("Raj", "Uh, crash-free sessions were 97 percent last week."),
    ], "crash_metrics", None, [],
     {"action_item": 0, "decision_made": 0, "factual_claim": 1, "open_question": 0,
      "agenda_item": "crash_metrics", "already_flagged": 0}),
    ("open question + pending answered", [
        ("Dana", "Who owns the app store screenshots?"),
        ("Raj", "Not me, I did them last time."),
        ("Mei", "Fine, I'll take the screenshots."),
    ], "store_assets", "Who owns the app store screenshots?", [],
     {"action_item": 1, "decision_made": 0, "factual_claim": 0, "open_question": 0,
      "answered_prior": 1, "agenda_item": "store_assets", "already_flagged": 0}),
    ("off agenda", [
        ("Raj", "Did anyone see the game last night?"),
        ("Dana", "Brutal. That last-minute penalty was robbed."),
        ("Mei", "Honestly the ref has had it in for us all season."),
    ], "launch_date", None, [],
     {"action_item": 0, "decision_made": 0, "factual_claim": 0, "open_question": 0,
      "agenda_item": "off_agenda", "already_flagged": 0}),
    ("already flagged", [
        ("Mei", "I'll send the revised deck to legal by Thursday."),
        ("Dana", "Great, thanks."),
        ("Mei", "Yep, so deck to legal Thursday, that's on me."),
    ], "store_assets", None, ["ACTION: Mei - send revised deck to legal - Thu"],
     {"action_item": 1, "decision_made": 0, "factual_claim": 0, "open_question": 0,
      "agenda_item": "store_assets", "already_flagged": 1}),
]


def render(lines, item, pending, flagged) -> str:
    w = RollingWindow(max_tokens=700)
    for spk, txt in lines:
        w.add(spk, txt)
    desc = dict(AGENDA)[item]
    header = {
        "AGENDA ITEM (current)": f"{item} - {desc}",
        "FACT SHEET KEYS": FACT_KEYS,
        "ALREADY FLAGGED": "; ".join(flagged) or "(none)",
    }
    if pending:
        header["PENDING"] = pending
    return w.render(header)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:8099")
    ap.add_argument("--repeat", type=int, default=5)
    ap.add_argument("--inproc", action="store_true", help="load the model in this process")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--model", default=None, help="checkpoint id or local path (inproc)")
    args = ap.parse_args()

    if args.inproc:
        kw = {"model_id": args.model} if args.model else {}
        dc = DeciderClient("inproc", device=args.device, **kw)
    else:
        dc = DeciderClient("http", url=args.url)
    print("health:", dc.health())
    dc.warmup()

    agree = total = 0
    lat: list[float] = []
    for name, lines, item, pending, flagged, expected in WINDOWS:
        state = render(lines, item, pending, flagged)
        qs = meeting_questions(AGENDA, pending_question=bool(pending))
        for _ in range(args.repeat):
            out = dc.ask(state, qs)
            lat.append(next(iter(out.values())).latency_ms)
        print(f"\n=== {name}  ({len(qs)} questions)")
        for k, d in out.items():
            exp = expected.get(k)
            if d.probs.keys() == {"true", "false"}:
                got, shown = int(d.p_true >= 0.5), f"P(true)={d.p_true:.3f}"
            else:
                got, shown = d.answer, f"{d.answer} ({d.confidence:.3f})"
            ok = exp is None or got == exp
            agree += ok
            total += 1
            print(f"  {'  ' if ok else 'XX'} {k:16s} {shown:32s} expected={exp}")
    lat.sort()
    print(f"\nagreement {agree}/{total}")
    print(f"latency per call ({len(lat)} calls, all questions batched): "
          f"p50={statistics.median(lat):.0f} ms  p95={lat[int(0.95 * (len(lat) - 1))]:.0f} ms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
