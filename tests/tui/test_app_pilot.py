# tests/tui/test_app_pilot.py
import shutil
from pathlib import Path

import pytest
from textual.widgets import TextArea
from textual.worker import WorkerCancelled

from pylings.app import PylingsApp
from pylings.widgets.editor_pane import EditorPane
from pylings.widgets.exercise_tree import ExerciseTree

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _work_copy(tmp_path: Path) -> Path:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    return work


async def _settle(pilot) -> None:
    """Let mount-time runs — and any chained auto-advance — finish.

    The first fixture exercise (`passing`) passes immediately, so on mount
    the app runs it, advances, and runs the next one. Each run is a thread
    worker; waiting for workers repeatedly drains the whole chain.

    WorkerCancelled is suppressed because exclusive=True workers cancel their
    predecessors; those cancellations are expected and safe to ignore here.
    """
    for _ in range(6):
        try:
            await pilot.app.workers.wait_for_complete()
        except WorkerCancelled:
            pass
        await pilot.pause()


@pytest.mark.asyncio
async def test_app_launches_and_shows_progress(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        progress = str(app.query_one("#progress").render())
        assert "/4" in progress


@pytest.mark.asyncio
async def test_welcome_message_is_shown_as_subtitle(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert app.sub_title == app.manifest.welcome_message


@pytest.mark.asyncio
async def test_editor_loads_current_exercise(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        current = app.state.current
        assert current is not None
        expected = (work / "exercises" / f"{current}.py").read_text(encoding="utf-8")
        assert app.query_one("#code", TextArea).text == expected


@pytest.mark.asyncio
async def test_output_header_names_the_exercise(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        header = str(app.query_one("#output-header").render())
        assert ".py" in header


@pytest.mark.asyncio
async def test_f1_toggles_hint(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        hint = app.query_one("#hint")
        assert "visible" not in hint.classes
        await pilot.press("f1")
        await pilot.pause()
        assert "visible" in hint.classes


@pytest.mark.asyncio
async def test_f3_toggles_tree(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        tree = app.query_one(ExerciseTree)
        before = tree.display
        await pilot.press("f3")
        await pilot.pause()
        assert tree.display != before


@pytest.mark.asyncio
async def test_ctrl_q_quits(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        await pilot.press("ctrl+q")


@pytest.mark.asyncio
async def test_f2_resets_current_file(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        current = app.state.current
        assert current is not None
        target = work / "exercises" / f"{current}.py"
        original = target.read_text(encoding="utf-8")

        # Use a syntax error so this never passes and advances to the next exercise.
        scrambled = "def broken(:\n    pass\n"
        app.query_one("#code", TextArea).text = scrambled
        app._flush_and_run()
        await _settle(pilot)
        assert target.read_text(encoding="utf-8") == scrambled

        await pilot.press("f2")
        await _settle(pilot)
        assert app.query_one("#code", TextArea).text == original
        assert target.read_text(encoding="utf-8") == original


@pytest.mark.asyncio
async def test_typing_triggers_autosave(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        current = app.state.current
        assert current is not None
        target = work / "exercises" / f"{current}.py"

        app.query_one("#code", TextArea).text = "raise SystemExit(7)\n"
        # Wait past the 0.6s debounce so the timer fires on its own.
        await pilot.pause(1.0)
        await _settle(pilot)
        assert target.read_text(encoding="utf-8") == "raise SystemExit(7)\n"


@pytest.mark.asyncio
async def test_solving_advances_to_next_exercise(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        before = app.state.current
        assert before is not None

        # A solution with no `# I AM NOT DONE` marker that exits 0.
        app.query_one("#code", TextArea).text = "assert 1 + 1 == 2\n"
        app._flush_and_run()
        await _settle(pilot)

        assert before in app.state.completed
        assert app.state.current != before
        # The editor has loaded whatever exercise is now current.
        if app.state.current is not None:
            loaded = (work / "exercises" / f"{app.state.current}.py").read_text(
                encoding="utf-8"
            )
            assert app.query_one("#code", TextArea).text == loaded
