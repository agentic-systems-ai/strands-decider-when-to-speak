"""The demo app serves its page and lists the prebuilt meetings (no Decider or LLM needed)."""

from fastapi.testclient import TestClient

from when_to_speak.app import app


def test_index_and_meetings():
    client = TestClient(app)
    assert "Knows When to Speak" in client.get("/").text
    rows = client.get("/api/meetings").json()
    assert len(rows) == 48
    assert {"id", "title", "split", "lines", "minutes"} <= set(rows[0])
    assert {r["split"] for r in rows} == {"dev", "test"}
