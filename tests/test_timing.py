from when_to_speak.schema import Persona, Turn
from when_to_speak.timing import build_timeline


def _p(name, wpm):
    return Persona(name=name, role="r", goals="g", hidden_agenda="h", verbosity=3, wpm=wpm)


def test_timeline_gaps_and_overlaps():
    personas = [_p("Dana", 150), _p("Raj", 130)]
    turns = [Turn(index=i, speaker="Dana" if i % 2 else "Raj", text="word " * (5 + i),
                  agenda_item="a", interrupted=(i == 3)) for i in range(10)]
    tl = build_timeline(turns, personas, seed=1)
    assert [t.turn_index for t in tl] == list(range(10))
    for i in range(1, 10):
        gap = tl[i].start_s - tl[i - 1].end_s
        if turns[i - 1].interrupted:
            assert -0.8 - 1e-6 <= gap < 0          # planned overlap
            assert tl[i].start_s > tl[i - 1].start_s
        else:
            assert 0.2 - 1e-6 <= gap <= 1.2 + 1e-6  # no negative gaps elsewhere
    # duration follows words / wpm
    d0 = tl[0].end_s - tl[0].start_s
    assert abs(d0 - 5 / (130 / 60)) < 1e-2


def test_timeline_deterministic():
    personas = [_p("Dana", 150)]
    turns = [Turn(index=i, speaker="Dana", text="hi there", agenda_item="a") for i in range(5)]
    assert build_timeline(turns, personas, seed=3) == build_timeline(turns, personas, seed=3)
