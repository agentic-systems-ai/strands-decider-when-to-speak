import pytest

from when_to_speak import providers
from when_to_speak.authored import AuthoringError, build, lint
from when_to_speak.dataset import windows

SRC = """---
meeting_id: t-1
theme: test
domain_pack: test_pack
drama: 0.5
seed: 3
pack:
  title: Test
  org: Testco
  agenda:
    - {id: a1, title: First, goal: g1, timebox_min: 1}
    - {id: a2, title: Second, goal: g2, timebox_min: 1}
  facts:
    - {id: F1, key: crash_free, statement: "Crash-free = 99.2%", value: "99.2%"}
personas:
  - {name: Maya, role: PM, goals: x, hidden_agenda: y, verbosity: 3, wpm: 160, voice_gender: female}
  - {name: Raj, role: Eng, goals: x, hidden_agenda: y, verbosity: 3, wpm: 150, voice_gender: male}
---
# a comment
## a1 :: opening
Maya: Crash-free was ninety-seven percent. {claim+ F1 "97%"}
Raj: It was ninety-nine point two. {claim- F1}
Maya: Did QA sign off? {question- @+1}
Raj: Yes, this morning.
## a2 :: wrap
Maya: I'll send the deck by Friday. {action+}
Raj: Did you see the game? {drift+ 2} {question- @+1}
Maya: Great game. So we're going with June 3rd, but I was going to say the—
Raj: Final, June 3rd. {decision+}
"""


def test_build_parses_tags_and_labels():
    m = build(SRC)
    assert [t.speaker for t in m.turns] == ["Maya", "Raj"] * 4
    by = {(g.category, g.polarity): g for g in m.gold}
    assert by[("factual_claim", "pos")].claimed_value == "97%"
    assert by[("factual_claim", "neg")].claimed_value == "99.2%"
    assert [g.resolution_turn for g in m.gold if g.category == "unanswered_question"] == [3, 6]
    assert by[("off_topic_drift", "pos")].span_turns == 2
    assert m.turns[6].interrupted and "{" not in m.turns[5].text
    assert m.turns[4].agenda_item == "a2"
    assert {p.polly_voice for p in m.cast.personas} and m.config["source"] == "authored"
    ws = list(windows(m))
    assert ws[0].labels["factual_claim"] and ws[1].labels["factual_claim"]
    assert ws[2].labels["open_question"] and ws[3].labels["answered_prior"]
    assert ws[4].labels["action_item"] and ws[7].labels["decision_made"]
    assert ws[5].labels["agenda_item"] == "off_agenda" == ws[6].labels["agenda_item"]
    assert ws[7].labels["agenda_item"] == "a2"
    assert not any("speaks twice" in w for w in lint(m))


@pytest.mark.parametrize("bad, msg", [
    ("Maya: Hi. {claim+ F9 \"1\"}", "known fact"),
    ("Maya: Hi? {question- }", "needs .@"),
    ("Zed: Hi.", "unknown speaker"),
    ("Maya: Hi. {claim+ F1}", "claimed"),
])
def test_build_rejects_bad_tags(bad, msg):
    with pytest.raises(AuthoringError, match=msg):
        build(SRC.replace("Raj: Final, June 3rd. {decision+}", bad))


def test_provider_switch(monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL_MAIN", raising=False)
    assert providers.provider() == "ollama" and providers.model_id() == "qwen3:8b"
    model = providers.strands_model()
    assert type(model).__name__ == "OllamaModel"
    monkeypatch.setenv("LLM_PROVIDER", "bedrock")
    monkeypatch.setenv("BEDROCK_MODEL_MAIN", "some-profile-id")
    assert providers.model_id("main") == "some-profile-id"
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    with pytest.raises(ValueError):
        providers.provider()


def test_fact_tokens_catch_spoken_restatements():
    from when_to_speak.authored import fact_tokens
    from when_to_speak.schema import Fact

    toks = fact_tokens([Fact(id="F1", key="k", statement="s", value="64%"),
                        Fact(id="F2", key="k", statement="s", value="August 9"),
                        Fact(id="F3", key="k", statement="s", value="$1,800"),
                        Fact(id="F4", key="k", statement="s", value="18,400")])
    assert {"64", "sixty-four", "august", "eighteen hundred", "one thousand eight hundred",
            "eighteen thousand four hundred"} <= toks
    assert "nine" not in toks  # small numbers are too common to flag


def test_spoken_forms_cover_shorthand_dates_and_times():
    from when_to_speak.authored import spoken_forms

    assert "twelve six" in spoken_forms("$12,600")[0]
    assert "three eighty" in spoken_forms("380")[0]
    assert "zero point six" in spoken_forms("0.6%")[0]
    assert "a hundred and twelve" in spoken_forms("112")[0]
    strong, weak = spoken_forms("September 25")
    assert "the twenty-fifth" in strong and "twenty-fifth" in weak
    assert "half two" in spoken_forms("2:30 pm")[1]
    assert "four" in spoken_forms("4")[1] and not spoken_forms("4")[0]
