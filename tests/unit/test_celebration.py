from __future__ import annotations

from pylings.screens.track import celebration_message


def test_celebration_message_includes_count_and_is_celebratory() -> None:
    msg = celebration_message(292)

    assert "292" in msg
    assert "🎉" in msg
