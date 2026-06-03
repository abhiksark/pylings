from __future__ import annotations

from pylings.screens.welcome import welcome_text


def test_welcome_text_explains_the_loop() -> None:
    text = welcome_text()

    # the core loop a beginner needs to understand
    assert "I AM NOT DONE" in text
    assert "save" in text.lower()
    # mentions at least one key shortcut
    assert "F1" in text
