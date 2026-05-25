from pathlib import Path

import pytest
from textual.app import App, ComposeResult
from textual.widgets import Static

from pylings.core.exercise import Exercise, RunResult
from pylings.widgets.output_panel import OutputPanel


class _Harness(App[None]):
    def compose(self) -> ComposeResult:
        yield OutputPanel()


def _exercise(
    tmp_path: Path,
    text: str,
    hint: str = "Use a string. Then remove the marker.",
    docs: str = "",
) -> Exercise:
    path = tmp_path / "variables1.py"
    path.write_text(text, encoding="utf-8")
    return Exercise(
        name="variables1",
        path=path,
        check_path=tmp_path / "check.py",
        topic="variables",
        hint=hint,
        docs=docs,
    )


def _result(
    exit_code: int,
    stdout: str = "",
    stderr: str = "",
    timed_out: bool = False,
) -> RunResult:
    return RunResult(
        passed=exit_code == 0 and not timed_out,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
        duration_s=0.1,
        timed_out=timed_out,
    )


@pytest.mark.asyncio
async def test_render_running_state(tmp_path: Path) -> None:
    app = _Harness()
    async with app.run_test() as pilot:
        await pilot.pause()
        panel = app.query_one(OutputPanel)
        panel.render_running(
            _exercise(tmp_path, "# Goal: set name\nname = broken\n"), 0, 2
        )
        await pilot.pause()
        assert "Running checks" in str(panel.query_one("#status", Static).content)


@pytest.mark.asyncio
async def test_failure_shows_goal_status_next_step_and_details(
    tmp_path: Path,
) -> None:
    app = _Harness()
    async with app.run_test() as pilot:
        await pilot.pause()
        panel = app.query_one(OutputPanel)
        ex = _exercise(tmp_path, "# Goal: set name\nname = broken\n")
        panel.render_result(
            ex,
            _result(1, stderr="NameError: broken"),
            failures=1,
            completed=0,
            total=2,
        )
        await pilot.pause()
        rendered = panel.renderable_text()
        assert "Goal" in rendered
        assert "set name" in rendered
        assert "Not passing yet" in rendered
        assert "NameError: broken" in rendered
        assert "Use a string." in rendered


@pytest.mark.asyncio
async def test_result_shows_docs_link(tmp_path: Path) -> None:
    app = _Harness()
    async with app.run_test() as pilot:
        await pilot.pause()
        panel = app.query_one(OutputPanel)
        ex = _exercise(
            tmp_path,
            "# Goal: set name\nname = broken\n",
            docs="https://docs.python.org/3/tutorial/introduction.html",
        )
        panel.render_result(ex, _result(1), failures=0, completed=0, total=2)
        await pilot.pause()
        rendered = panel.renderable_text()
        assert "Docs" in rendered
        assert "https://docs.python.org/3/tutorial/introduction.html" in rendered


@pytest.mark.asyncio
async def test_marker_pass_prompts_marker_removal(tmp_path: Path) -> None:
    app = _Harness()
    async with app.run_test() as pilot:
        await pilot.pause()
        panel = app.query_one(OutputPanel)
        ex = _exercise(tmp_path, "# I AM NOT DONE\nvalue = 1\n")
        panel.render_result(
            ex, _result(0, stdout="ok"), failures=0, completed=0, total=2
        )
        await pilot.pause()
        assert "remove marker" in panel.renderable_text().lower()


@pytest.mark.asyncio
async def test_full_hint_toggles_on_f1(tmp_path: Path) -> None:
    app = _Harness()
    async with app.run_test() as pilot:
        await pilot.pause()
        panel = app.query_one(OutputPanel)
        panel.toggle_hint("Full hint text.")
        await pilot.pause()
        assert "Full hint text." in str(panel.query_one("#hint", Static).content)
