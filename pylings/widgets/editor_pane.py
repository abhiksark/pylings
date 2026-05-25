# pylings/widgets/editor_pane.py
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import TextArea

from pylings.core.exercise import Exercise


class EditorPane(Vertical):
    """The in-TUI code editor for the current exercise."""

    def compose(self) -> ComposeResult:
        try:
            editor = TextArea.code_editor("", language="python", id="code")
        except Exception:
            # tree-sitter Python grammar unavailable — fall back to plain text.
            editor = TextArea.code_editor("", id="code")
        yield editor

    def load_exercise(self, exercise: Exercise) -> None:
        """Replace the editor contents with the exercise file from disk."""
        area = self.query_one("#code", TextArea)
        area.text = exercise.path.read_text(encoding="utf-8")
        area.move_cursor((0, 0))

    def focus_editor(self) -> None:
        self.query_one("#code", TextArea).focus()

    @property
    def text(self) -> str:
        return self.query_one("#code", TextArea).text
