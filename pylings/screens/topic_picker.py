# pylings/screens/topic_picker.py
from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, ListItem, ListView, Static


class TopicPickerScreen(Screen[None]):
    """Entry screen: choose a topic to work on."""

    BINDINGS = [Binding("ctrl+q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(ListView(id="topics"))
        yield Footer()

    def on_mount(self) -> None:
        self.app.title = "pylings"
        self.app.sub_title = "choose a topic"
        self._populate()

    def on_screen_resume(self) -> None:
        self._populate()

    def _populate(self) -> None:
        listview = self.query_one("#topics", ListView)
        listview.clear()
        manifest = self.app.manifest
        completed = self.app.state.completed
        for topic in manifest.topics():
            exs = manifest.exercises_in(topic)
            done = sum(1 for ex in exs if ex.name in completed)
            if done == len(exs):
                mark = "✓"
            elif done:
                mark = "●"
            else:
                mark = " "
            label = f"{mark}  {topic:<18} {done}/{len(exs)}"
            listview.append(
                ListItem(Static(label, classes="topic-row"), name=topic)
            )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        topic = event.item.name
        if topic:
            from pylings.screens.track import TrackScreen

            self.app.push_screen(TrackScreen(topic))
