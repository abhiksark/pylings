# pythonlings/screens/topic_picker.py
from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, ListItem, ListView, Static

from pythonlings.core.state import save as save_state


class TopicPickerScreen(Screen[None]):
    """Entry screen: choose a topic to work on."""

    BINDINGS = [
        Binding("escape", "quit", "Quit", priority=True),
        Binding("ctrl+q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("", id="topic-banner")
        yield VerticalScroll(ListView(id="topics"))
        yield Footer()

    def on_mount(self) -> None:
        self.app.title = "pythonlings"
        self.app.sub_title = "choose a topic"
        self._populate()

    def on_screen_resume(self) -> None:
        self._populate()

    def _populate(self) -> None:
        listview = self.query_one("#topics", ListView)
        listview.clear()
        self.query_one("#topic-banner", Static).update(self._banner_text())
        manifest = self.app.manifest
        completed = self.app.state.completed
        selected_index = 0
        preferred = self._preferred_topic()
        for topic_index, topic in enumerate(manifest.topics()):
            exs = manifest.exercises_in(topic)
            done = sum(1 for ex in exs if ex.name in completed)
            if done == len(exs):
                mark = "✓"
                status = "Done"
            elif done:
                mark = "●"
                status = "Continue"
            else:
                mark = " "
                status = "Start"
            label = f"{mark}  {topic:<18} {done}/{len(exs):<5} {status}"
            listview.append(
                ListItem(Static(label, classes="topic-row"), name=topic)
            )
            if topic == preferred:
                selected_index = topic_index
        if listview.children:
            listview.index = selected_index
            listview.focus()

    def _topic_progress(self, topic: str) -> tuple[int, int]:
        exs = self.app.manifest.exercises_in(topic)
        done = sum(1 for ex in exs if ex.name in self.app.state.completed)
        return done, len(exs)

    def _first_incomplete_topic(self) -> str | None:
        for topic in self.app.manifest.topics():
            done, total = self._topic_progress(topic)
            if done < total:
                return topic
        return None

    def _preferred_topic(self) -> str | None:
        topic = self.app.state.last_topic
        if topic in self.app.manifest.topics():
            done, total = self._topic_progress(topic)
            if done < total:
                return topic
        return self._first_incomplete_topic() or (
            self.app.manifest.topics()[0] if self.app.manifest.topics() else None
        )

    def _banner_text(self) -> str:
        first = self._first_incomplete_topic()
        if first is None:
            return self.app.manifest.final_message
        if not self.app.state.seen_intro:
            return f"Start here: {first}"
        if self.app.state.last_topic is None:
            return "Choose a topic to practice."
        return "Topics"

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        topic = event.item.name
        if topic:
            from pythonlings.screens.track import TrackScreen

            self.app.state.record_resume(topic, None)
            save_state(self.app.root, self.app.state)
            self.app.push_screen(TrackScreen(topic))

    def action_quit(self) -> None:
        self.app.exit(0)
