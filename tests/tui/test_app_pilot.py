# tests/tui/test_app_pilot.py
import shutil
from pathlib import Path

import pytest

from pylings.app import PylingsApp

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


@pytest.mark.asyncio
async def test_app_launches_and_shows_first_exercise(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await pilot.pause()
        progress = pilot.app.query_one("#progress")
        rendered = str(progress.render())
        assert "0/4" in rendered or "1/4" in rendered


@pytest.mark.asyncio
async def test_h_binding_toggles_hint(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await pilot.pause()
        hint = pilot.app.query_one("#hint")
        assert "visible" not in hint.classes
        await pilot.press("h")
        await pilot.pause()
        assert "visible" in hint.classes


@pytest.mark.asyncio
async def test_q_binding_quits(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await pilot.pause()
        await pilot.press("q")


@pytest.mark.asyncio
async def test_r_binding_resets_current_file(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await pilot.pause()
        # Whichever exercise the app settled on after auto-advancing.
        current_name = pilot.app.state.current
        assert current_name is not None
        target = work / "exercises" / f"{current_name}.py"
        original = target.read_text()
        target.write_text("# scrambled\n", encoding="utf-8")

        await pilot.press("r")
        await pilot.pause()
        assert target.read_text() == original


@pytest.mark.asyncio
async def test_l_binding_toggles_tree_visibility(tmp_path: Path) -> None:
    from pylings.widgets.exercise_tree import ExerciseTree

    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await pilot.pause()
        tree = pilot.app.query_one(ExerciseTree)
        before = tree.display
        await pilot.press("l")
        await pilot.pause()
        assert tree.display != before


@pytest.mark.asyncio
async def test_output_panel_shows_file_path_and_instruction(tmp_path: Path) -> None:
    # The output panel must tell the learner which file to edit and what to do
    # with it — otherwise the TUI is just an unexplained traceback.
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await pilot.pause()
        header = str(pilot.app.query_one("#output-header").render())
        assert ".py" in header
        assert "Open the file" in header


@pytest.mark.asyncio
async def test_welcome_message_is_shown_as_subtitle(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await pilot.pause()
        assert pilot.app.sub_title == pilot.app.manifest.welcome_message


@pytest.mark.asyncio
async def test_n_binding_is_a_noop_outside_animation(tmp_path: Path) -> None:
    # Smoke test only: pressing n must not crash, and state should be unchanged.
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await pilot.pause()
        completed_before = set(pilot.app.state.completed)
        current_before = pilot.app.state.current
        await pilot.press("n")
        await pilot.pause()
        assert pilot.app.state.completed == completed_before
        assert pilot.app.state.current == current_before
