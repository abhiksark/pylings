# tests/tui/test_editor_pane.py
from pathlib import Path

import pytest
from textual.app import App, ComposeResult
from textual.widgets import TextArea

from pylings.core.exercise import Exercise
from pylings.widgets.editor_pane import EditorPane


class _Harness(App[None]):
    def compose(self) -> ComposeResult:
        yield EditorPane()


@pytest.mark.asyncio
async def test_load_exercise_fills_editor(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("a = 1\nb = 2\n", encoding="utf-8")
    exercise = Exercise(
        name="ex",
        path=file,
        check_path=tmp_path / "check.py",
        topic="t",
        hint="",
    )

    app = _Harness()
    async with app.run_test() as pilot:
        await pilot.pause()
        pane = app.query_one(EditorPane)
        pane.load_exercise(exercise)
        await pilot.pause()
        assert pane.text == "a = 1\nb = 2\n"


@pytest.mark.asyncio
async def test_text_property_reflects_buffer(tmp_path: Path) -> None:
    app = _Harness()
    async with app.run_test() as pilot:
        await pilot.pause()
        pane = app.query_one(EditorPane)
        pane.query_one("#code", TextArea).text = "x = 42\n"
        await pilot.pause()
        assert pane.text == "x = 42\n"


@pytest.mark.asyncio
async def test_focus_editor_focuses_the_text_area(tmp_path: Path) -> None:
    app = _Harness()
    async with app.run_test() as pilot:
        await pilot.pause()
        pane = app.query_one(EditorPane)
        pane.focus_editor()
        await pilot.pause()
        assert app.focused is pane.query_one("#code", TextArea)
