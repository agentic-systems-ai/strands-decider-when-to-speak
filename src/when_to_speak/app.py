"""Demo app: replay a meeting through the agent and watch every decision live.

    python -m when_to_speak.app                     # http://127.0.0.1:8080, Decider at DECIDER_URL
    python -m when_to_speak.app --decider fake      # no GPU: scripted decisions (UI work)

One WebSocket per browser tab. The browser sends {"cmd": "start", "meeting": id, "speed": 2,
"mode": "gated" | "ungated"} and then "pause", "resume", "speed" or "stop"; the server streams
"meeting", "line", "gate", "card", "speak", "tick", "stats" and "done" events.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import statistics
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse

from .agent import DEFAULT_THRESHOLDS, MeetingAgent
from .dataset import load_meetings
from .replay import utterances
from .scoring import score_meeting

ROOT = Path(__file__).resolve().parents[2]
STATIC = Path(__file__).resolve().parent / "static"
MEETINGS_DIR = Path(os.environ.get("MEETINGS_DIR", ROOT / "data" / "meetings"))
# Bedrock list prices per million tokens (us-east-2, global; AWS Pricing API, Oct 2026), for the
# "same tokens at a bigger model" line in the stats bar. "frontier" is Claude Sonnet 5.5's price.
PRICES = {"gpt-oss-20b": (0.07, 0.30), "frontier": (2.0, 10.0)}

app = FastAPI(title="Knows When to Speak")
_decider_kind = os.environ.get("DEMO_DECIDER", "http")
_meetings: dict[str, Any] = {}
_splits: dict[str, str] = {}


def meetings() -> dict[str, Any]:
    if not _meetings:
        test_ids = set()
        test_file = ROOT / "data" / "windows" / "test.jsonl"
        if test_file.exists():
            test_ids = {json.loads(line)["meeting_id"] for line in test_file.read_text().splitlines()}
        for m in load_meetings(MEETINGS_DIR):
            _splits[m.meeting_id] = "test" if m.meeting_id in test_ids else "dev"
            _meetings[m.meeting_id] = m
    return _meetings


def make_decider():
    if _decider_kind == "fake":
        from decider_client import FakeDeciderClient

        return FakeDeciderClient(_fake_script, latency_ms=40.0)
    from decider_client import DeciderClient

    client = DeciderClient()
    client.warmup()
    return client


def _fake_script(state: str, q) -> Any:
    """Rough keyword decisions so the UI can be built without a GPU."""
    latest = state.splitlines()[-1].lower()
    rules = {"action_item": ("i'll", "i will"), "decision_made": ("let's go with", "decided", "agreed"),
             "factual_claim": tuple("0123456789"), "open_question": ("?",), "off_agenda": ("weekend", "game")}
    if q.key in rules:
        return 0.9 if any(k in latest for k in rules[q.key]) else 0.05
    if q.key == "answered_prior":
        return 0.5
    return 0.02


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


@app.get("/api/meetings")
def list_meetings() -> JSONResponse:
    out = [{"id": m.meeting_id, "title": m.cast.pack.title, "org": m.cast.pack.org, "split": _splits[m.meeting_id],
            "lines": len(m.timeline), "minutes": round(m.timeline[-1].end_s / 60, 1)}
           for m in meetings().values()]
    return JSONResponse(sorted(out, key=lambda r: r["id"]))


class Run:
    """One meeting replay for one WebSocket."""

    def __init__(self, ws: WebSocket, meeting, speed: float, gated: bool):
        self.ws = ws
        self.m = meeting
        self.speed = speed
        self.gated = gated
        self.paused = asyncio.Event()
        self.paused.set()  # set = running
        self.stopped = False
        self.loop = asyncio.get_running_loop()
        self.queue: asyncio.Queue = asyncio.Queue()
        self.decider_ms: list[float] = []
        self.counts = {"lines": 0, "wakes": 0, "spoken": 0, "notes": 0}

    def emit(self, kind: str, payload: dict) -> None:
        """Called from the agent's worker thread."""
        self.loop.call_soon_threadsafe(self.queue.put_nowait, {"type": kind, **payload})

    async def pump(self) -> None:
        while True:
            msg = await self.queue.get()
            if msg is None:
                return
            await self.ws.send_json(msg)

    def stats(self, agent: MeetingAgent) -> dict:
        u = agent.llm_usage
        lines = self.counts["lines"]
        cost = {name: (u["input_tokens"] * pi + u["output_tokens"] * po) / 1e6
                for name, (pi, po) in PRICES.items()}
        return {"type": "stats", **self.counts,
                "skipped_pct": 100 * (1 - self.counts["wakes"] / lines) if lines else 0.0,
                "decider_p50": statistics.median(self.decider_ms) if self.decider_ms else 0.0,
                "input_tokens": u["input_tokens"], "output_tokens": u["output_tokens"], "cost": cost}

    async def run(self) -> None:
        pump = asyncio.create_task(self.pump())
        try:
            decider = await asyncio.to_thread(make_decider) if self.gated else None
            agent = MeetingAgent(self.m.cast.pack, decider, emit=self.emit, gated=self.gated)
            await self.ws.send_json(self.meeting_event())
            prev_t = 0.0
            for u in utterances(self.m):
                # Wait out the gap since the previous line ended, at the chosen speed.
                gap = max(0.0, u.t_end - prev_t)
                prev_t = u.t_end
                waited = 0.0
                while waited < gap / max(self.speed, 0.1):
                    await self.paused.wait()
                    if self.stopped:
                        return
                    await asyncio.sleep(0.05)
                    waited += 0.05
                await self.paused.wait()
                if self.stopped:
                    return
                agent.state.now = u.t_end  # so the agenda header is right before the tick
                self.emit("line", {"turn_index": u.turn_index, "speaker": u.speaker, "text": u.text,
                                   "t": u.t_end, "agenda_index": agent.state.scheduled_item(u.t_end)})
                tr = await asyncio.to_thread(agent.on_utterance, u)
                self.counts["lines"] += 1
                self.counts["wakes"] += tr.woke_llm
                self.counts["spoken"] += tr.spoken is not None
                self.counts["notes"] += sum(c.kind == "note" for c in tr.cards)
                if self.gated:
                    self.decider_ms.append(tr.decider_ms)
                self.queue.put_nowait(self.stats(agent))
            s = score_meeting(self.m, agent.ticks)
            self.queue.put_nowait({"type": "done", "score": {
                c: {"tp": cs.tp, "fp": cs.fp, "fn": cs.fn} for c, cs in s.per_category.items()},
                "unjustified": s.unjustified_spoken, "spoken": s.spoken})
        except Exception as e:  # shown in the UI instead of a silent hang
            self.queue.put_nowait({"type": "error", "message": f"{type(e).__name__}: {e}"})
            raise
        finally:
            self.queue.put_nowait(None)
            await pump

    def meeting_event(self) -> dict:
        m = self.m
        pack = m.cast.pack
        gold: dict[int, list[dict]] = {}
        for g in m.gold:
            gold.setdefault(g.turn_index, []).append({"category": g.category, "polarity": g.polarity})
        return {"type": "meeting", "id": m.meeting_id, "title": pack.title, "org": pack.org,
                "gated": self.gated, "lines": len(m.timeline),
                "agenda": [a.model_dump() for a in pack.agenda],
                "facts": [f.model_dump() for f in pack.facts],
                "personas": [{"name": p.name, "role": p.role, "color": p.avatar_color} for p in m.cast.personas],
                "thresholds": {k: {"speak": t.speak, "note": t.note} for k, t in DEFAULT_THRESHOLDS.items()},
                "gold": gold}


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    run: Run | None = None
    task: asyncio.Task | None = None
    try:
        while True:
            msg = await ws.receive_json()
            cmd = msg.get("cmd")
            if cmd == "start":
                if run:
                    run.stopped = True
                    run.paused.set()
                if task:
                    await asyncio.gather(task, return_exceptions=True)
                m = meetings().get(msg.get("meeting"))
                if m is None:
                    await ws.send_json({"type": "error", "message": f"unknown meeting {msg.get('meeting')!r}"})
                    continue
                run = Run(ws, m, float(msg.get("speed", 2)), msg.get("mode", "gated") != "ungated")
                task = asyncio.create_task(run.run())
            elif run and cmd == "pause":
                run.paused.clear()
            elif run and cmd == "resume":
                run.paused.set()
            elif run and cmd == "speed":
                run.speed = float(msg.get("value", 1))
            elif run and cmd == "stop":
                run.stopped = True
                run.paused.set()
    except WebSocketDisconnect:
        if run:
            run.stopped = True
            run.paused.set()


def main() -> int:
    global _decider_kind
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=int(os.environ.get("APP_PORT", 8080)))
    ap.add_argument("--decider", choices=["http", "fake"], default=_decider_kind)
    args = ap.parse_args()
    _decider_kind = args.decider
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    import uvicorn

    uvicorn.run(app, host=args.host, port=args.port, log_level="info")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
