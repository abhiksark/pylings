# pylings/app.py
from __future__ import annotations

from pathlib import Path

from textual.app import App

from pylings.core.manifest import Manifest, load as load_manifest
from pylings.core.state import State, load as load_state, next_pending
from pylings.screens.topic_picker import TopicPickerScreen
from pylings.screens.track import TrackScreen


class PylingsApp(App[int]):
    CSS_PATH = "pylings.tcss"

    def __init__(
        self,
        root: Path,
        start_topic: str | None = None,
        force_picker: bool = False,
        watch_files: bool = False,
    ) -> None:
        super().__init__()
        self.root = root
        self.manifest: Manifest = load_manifest(root)
        self.state: State = load_state(root)
        self._start_topic = start_topic
        self._force_picker = force_picker
        self.watch_files = watch_files

    def on_mount(self) -> None:
        first_launch = not self.state.seen_intro
        self.push_screen(TopicPickerScreen())
        target = self._startup_target()
        if target is not None:
            topic, exercise = target
            self.push_screen(TrackScreen(topic, start_exercise=exercise))
        if first_launch and target is not None:
            from pylings.screens.welcome import WelcomeScreen

            self.push_screen(WelcomeScreen())

    def _startup_target(self) -> tuple[str, str | None] | None:
        if self._start_topic is not None:
            if self._start_topic in self.manifest.topics():
                return self._start_topic, None
            return None
        if self._force_picker:
            return None
        return self._resume_target() or self._first_pending_target()

    def _resume_target(self) -> tuple[str, str | None] | None:
        topic = self.state.last_topic
        if topic not in self.manifest.topics():
            return None

        exercises = self.manifest.exercises_in(topic)
        names = {ex.name for ex in exercises}
        last = self.state.last_exercise
        if last in names and last not in self.state.completed:
            return topic, last

        next_name = next_pending(exercises, self.state.completed)
        if next_name is not None:
            return topic, next_name
        return None

    def _first_pending_target(self) -> tuple[str, str | None] | None:
        for topic in self.manifest.topics():
            next_name = next_pending(
                self.manifest.exercises_in(topic), self.state.completed
            )
            if next_name is not None:
                return topic, next_name
        return None


def run_tui(
    root: Path,
    start_topic: str | None = None,
    force_picker: bool = False,
    watch_files: bool = False,
) -> int:
    return (
        PylingsApp(
            root,
            start_topic,
            force_picker=force_picker,
            watch_files=watch_files,
        ).run()
        or 0
    )
