# tests/tui/test_app_pilot.py
import shutil
import webbrowser
from pathlib import Path

import pytest
from textual.widgets import Markdown, Static, TextArea
from textual.worker import WorkerCancelled

from pythonlings.app import PythonlingsApp
from pythonlings.core.state import State, save as save_state
from pythonlings.screens.docs import DocsScreen
from pythonlings.screens.topic_picker import TopicPickerScreen
from pythonlings.screens.track import TrackScreen
from pythonlings.widgets.output_panel import OutputPanel

MULTI = Path(__file__).parent.parent / "fixtures" / "multi_topic"


def _work_copy(tmp_path: Path) -> Path:
    work = tmp_path / "work"
    shutil.copytree(MULTI, work, ignore=shutil.ignore_patterns(".pythonlings"))
    return work


async def _settle(pilot) -> None:
    for _ in range(6):
        try:
            await pilot.app.workers.wait_for_complete()
        except WorkerCancelled:
            pass
        await pilot.pause()


@pytest.mark.asyncio
async def test_default_launch_opens_first_pending_exercise(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        assert app.screen.topic == "alpha"
        assert app.screen.current == "a1"


@pytest.mark.asyncio
async def test_picker_lists_topics_with_progress(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), force_picker=True)
    async with app.run_test() as pilot:
        await _settle(pilot)
        rendered = " ".join(
            str(row.content) for row in app.screen.query(".topic-row").results()
        )
        assert "alpha" in rendered
        assert "beta" in rendered


@pytest.mark.asyncio
async def test_enter_on_picker_opens_selected_topic(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), force_picker=True)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TopicPickerScreen)
        await pilot.press("enter")
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        assert app.screen.topic == "alpha"
        assert app.screen.current == "a1"


@pytest.mark.asyncio
async def test_picker_shows_first_run_start_banner(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), force_picker=True)
    async with app.run_test() as pilot:
        await _settle(pilot)
        banner = str(app.screen.query_one("#topic-banner").content)
        assert "Start here" in banner
        assert "alpha" in banner


@pytest.mark.asyncio
async def test_picker_rows_show_status_labels(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    save_state(work, State(completed={"a1"}, seen_intro=True, last_topic="alpha"))
    app = PythonlingsApp(root=work, force_picker=True)
    async with app.run_test() as pilot:
        await _settle(pilot)
        rendered = " ".join(
            str(row.content)
            for row in app.screen.query(".topic-row").results()
        )
        assert "Continue" in rendered
        assert "Start" in rendered


@pytest.mark.asyncio
async def test_start_topic_opens_track(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        assert app.screen.topic == "alpha"


@pytest.mark.asyncio
async def test_default_launch_resumes_last_incomplete_exercise(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    save_state(
        work,
        State(seen_intro=True, last_topic="alpha", last_exercise="a2"),
    )
    app = PythonlingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        assert app.screen.topic == "alpha"
        assert app.screen.current == "a2"


@pytest.mark.asyncio
async def test_default_launch_falls_back_from_invalid_resume_state(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    save_state(
        work,
        State(seen_intro=True, last_topic="missing", last_exercise="ghost"),
    )
    app = PythonlingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        assert app.screen.topic == "alpha"
        assert app.screen.current == "a1"


@pytest.mark.asyncio
async def test_force_picker_launch_ignores_resume_state(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    save_state(
        work,
        State(seen_intro=True, last_topic="alpha", last_exercise="a2"),
    )
    app = PythonlingsApp(root=work, force_picker=True)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TopicPickerScreen)


@pytest.mark.asyncio
async def test_f4_returns_to_picker(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        await pilot.press("f4")
        await pilot.pause()
        assert isinstance(app.screen, TopicPickerScreen)


@pytest.mark.asyncio
async def test_escape_quits_from_track_screen(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        await pilot.press("escape")
        await pilot.pause()
        assert app.return_code == 0


@pytest.mark.asyncio
async def test_escape_quits_from_topic_picker(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), force_picker=True)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TopicPickerScreen)
        await pilot.press("escape")
        await pilot.pause()
        assert app.return_code == 0


@pytest.mark.asyncio
async def test_f5_opens_docs_popup_for_current_exercise(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        await pilot.press("f5")
        await pilot.pause()
        assert isinstance(app.screen, DocsScreen)
        assert "a1" in str(app.screen.query_one("#docs-title", Static).content)
        rendered = app.screen.query_one("#docs-content", Markdown)._markdown
        assert "Local reference" in rendered
        assert "# Variables" not in rendered
        assert "Assigning names" in rendered
        assert "https://docs.python.org/3/tutorial/introduction.html" in rendered
        footer = app.screen.query_one("#docs-footer", Static).content
        assert "O Open official docs" in str(footer)
        assert "Esc Close" in str(footer)


@pytest.mark.asyncio
async def test_escape_closes_docs_popup_without_quitting(tmp_path: Path) -> None:
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        await pilot.press("f5")
        await pilot.pause()
        assert isinstance(app.screen, DocsScreen)
        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, TrackScreen)
        assert app.return_code is None


@pytest.mark.asyncio
async def test_docs_popup_can_open_browser(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    opened: list[str] = []
    monkeypatch.setattr(webbrowser, "open", lambda url: opened.append(url))
    app = PythonlingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        await pilot.press("f5")
        await pilot.pause()
        assert isinstance(app.screen, DocsScreen)
        await pilot.press("o")
        await pilot.pause()
        assert opened == ["https://docs.python.org/3/tutorial/introduction.html"]


@pytest.mark.asyncio
async def test_track_records_resume_when_loaded(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert app.state.seen_intro is True
        assert app.state.last_topic == "alpha"
        assert app.state.last_exercise == "a1"


@pytest.mark.asyncio
async def test_instant_advance_updates_resume_to_next_exercise(
    tmp_path: Path,
) -> None:
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        track.query_one("#code", TextArea).text = "x = 1\n"
        track._flush_and_run()
        await _settle(pilot)
        assert "a1" in app.state.completed
        assert track.current == "a2"
        assert app.state.last_topic == "alpha"
        assert app.state.last_exercise == "a2"


@pytest.mark.asyncio
async def test_failed_run_shows_progressive_nudge(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        track.query_one("#code", TextArea).text = "x = 99\n"
        track._flush_and_run()
        await _settle(pilot)
        assert "alpha one" in track.query_one(OutputPanel).renderable_text()


@pytest.mark.asyncio
async def test_hint_visibility_resets_after_advance(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        track.action_toggle_hint()
        await pilot.pause()
        assert "visible" in track.query_one("#hint").classes

        track.query_one("#code", TextArea).text = "x = 1\n"
        track._flush_and_run()
        await _settle(pilot)
        assert track.current == "a2"
        assert "visible" not in track.query_one("#hint").classes


@pytest.mark.asyncio
async def test_solving_a_topic_marks_progress(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="beta")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        # beta has one exercise, b1; solve it.
        track.query_one("#code", TextArea).text = "z = 3\n"
        track._flush_and_run()
        await _settle(pilot)
        assert "b1" in app.state.completed


@pytest.mark.asyncio
async def test_picker_refreshes_progress_after_returning(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PythonlingsApp(root=work, start_topic="beta")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        track.query_one("#code", TextArea).text = "z = 3\n"
        track._flush_and_run()
        await _settle(pilot)
        await pilot.press("f4")
        await _settle(pilot)
        assert isinstance(app.screen, TopicPickerScreen)
        rendered = " ".join(
            str(row.content)
            for row in app.screen.query(".topic-row").results()
        )
        # beta's one exercise is now done -> "1/1" must appear.
        assert "1/1" in rendered
