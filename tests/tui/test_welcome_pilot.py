import shutil
from pathlib import Path

import pytest
from textual.worker import WorkerCancelled

from pylings.app import PylingsApp
from pylings.core.state import State, load as load_state, save as save_state
from pylings.screens.track import TrackScreen
from pylings.screens.welcome import WelcomeScreen

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
async def test_welcome_shown_on_first_launch(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, WelcomeScreen)


@pytest.mark.asyncio
async def test_welcome_not_shown_after_intro_seen(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    save_state(work, State(seen_intro=True))

    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert not isinstance(app.screen, WelcomeScreen)
        assert isinstance(app.screen, TrackScreen)


@pytest.mark.asyncio
async def test_dismissing_welcome_persists_seen_intro(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)

    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, WelcomeScreen)
        await pilot.press("enter")
        await _settle(pilot)
        assert not isinstance(app.screen, WelcomeScreen)

    assert load_state(work).seen_intro is True
