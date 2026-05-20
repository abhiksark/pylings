# pylings/app.py
from __future__ import annotations

from pathlib import Path

from textual.app import App

from pylings.core.manifest import Manifest, load as load_manifest
from pylings.core.state import State, load as load_state
from pylings.screens.topic_picker import TopicPickerScreen
from pylings.screens.track import TrackScreen


class PylingsApp(App[int]):
    CSS_PATH = "pylings.tcss"

    def __init__(self, root: Path, start_topic: str | None = None) -> None:
        super().__init__()
        self.root = root
        self.manifest: Manifest = load_manifest(root)
        self.state: State = load_state(root)
        self._start_topic = start_topic

    def on_mount(self) -> None:
        self.push_screen(TopicPickerScreen())
        if self._start_topic is not None and self._start_topic in self.manifest.topics():
            self.push_screen(TrackScreen(self._start_topic))


def run_tui(root: Path, start_topic: str | None = None) -> int:
    return PylingsApp(root, start_topic).run() or 0
