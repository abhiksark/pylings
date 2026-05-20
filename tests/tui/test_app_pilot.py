# tests/tui/test_app_pilot.py
import shutil
from pathlib import Path

import pytest
from textual.widgets import TextArea
from textual.worker import WorkerCancelled

from pylings.app import PylingsApp
from pylings.screens.topic_picker import TopicPickerScreen
from pylings.screens.track import TrackScreen

MULTI = Path(__file__).parent.parent / "fixtures" / "multi_topic"


def _work_copy(tmp_path: Path) -> Path:
    work = tmp_path / "work"
    shutil.copytree(MULTI, work, ignore=shutil.ignore_patterns(".pylings"))
    return work


async def _settle(pilot) -> None:
    for _ in range(6):
        try:
            await pilot.app.workers.wait_for_complete()
        except WorkerCancelled:
            pass
        await pilot.pause()


@pytest.mark.asyncio
async def test_launches_on_topic_picker(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TopicPickerScreen)


@pytest.mark.asyncio
async def test_picker_lists_topics_with_progress(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        rendered = " ".join(
            str(row.content) for row in app.screen.query(".topic-row").results()
        )
        assert "alpha" in rendered
        assert "beta" in rendered


@pytest.mark.asyncio
async def test_start_topic_opens_track(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        assert app.screen.topic == "alpha"


@pytest.mark.asyncio
async def test_f4_returns_to_picker(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        await pilot.press("f4")
        await pilot.pause()
        assert isinstance(app.screen, TopicPickerScreen)


@pytest.mark.asyncio
async def test_solving_a_topic_marks_progress(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PylingsApp(root=work, start_topic="beta")
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
    app = PylingsApp(root=work, start_topic="beta")
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
