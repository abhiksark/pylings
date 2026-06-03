from __future__ import annotations

from pylings.widgets.progress import format_progress


def test_format_progress_shows_topic_and_overall() -> None:
    line = format_progress(2, 5, 10, 100)

    # topic portion: 2/5 == 40%
    assert "2/5" in line
    assert "40%" in line
    # overall portion: 10/100 == 10%
    assert "10/100" in line
    assert "10%" in line
    assert "Overall" in line


def test_format_progress_handles_zero_totals() -> None:
    line = format_progress(0, 0, 0, 0)

    assert "0/0" in line
    assert "0%" in line
