# pylings/screens/track.py
from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Footer, Header, TextArea

from pylings.core.exercise import Exercise, RunResult
from pylings.core.runner import run as run_exercise
from pylings.core.state import next_pending, save as save_state
from pylings.widgets.editor_pane import EditorPane
from pylings.widgets.exercise_tree import ExerciseTree
from pylings.widgets.output_panel import OutputPanel
from pylings.widgets.progress import ProgressBar

_DEBOUNCE_SECONDS = 0.6


class TrackScreen(Screen[None]):
    """One topic's linear track: editor + output + auto-save loop."""

    BINDINGS = [
        Binding("f1", "toggle_hint", "Hint"),
        Binding("f2", "reset", "Reset"),
        Binding("f3", "toggle_list", "List"),
        Binding("f4", "topics", "Topics"),
        Binding("ctrl+q", "quit", "Quit"),
    ]

    def __init__(self, topic: str) -> None:
        super().__init__()
        self.topic = topic
        self._save_timer: Timer | None = None
        self._loaded_text = ""
        self.current: str | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield ProgressBar(id="progress")
        yield Horizontal(
            ExerciseTree(),
            EditorPane(id="editor"),
            OutputPanel(id="output"),
            id="main",
        )
        yield Footer()

    def on_mount(self) -> None:
        self.app.sub_title = f"topic: {self.topic}"
        self.current = next_pending(self._exercises(), self.app.state.completed)
        self._render_state()
        if self.current is None:
            self.query_one(OutputPanel).show_final(
                f"Topic '{self.topic}' complete."
            )
            return
        self._load_current()
        self._run_current()
        self.query_one(EditorPane).focus_editor()

    # --- helpers ---------------------------------------------------------

    def _exercises(self) -> list[Exercise]:
        return self.app.manifest.exercises_in(self.topic)

    def _render_state(self) -> None:
        exs = self._exercises()
        done = sum(1 for ex in exs if ex.name in self.app.state.completed)
        self.query_one(ProgressBar).update_progress(done, len(exs))
        self.query_one(ExerciseTree).render_topic(
            self.topic, exs, self.app.state.completed, self.current
        )

    def _exercise(self, name: str) -> Exercise:
        for ex in self._exercises():
            if ex.name == name:
                return ex
        raise KeyError(name)

    def _load_current(self) -> None:
        if self.current is None:
            return
        if self._save_timer is not None:
            self._save_timer.stop()
            self._save_timer = None
        pane = self.query_one(EditorPane)
        pane.load_exercise(self._exercise(self.current))
        self._loaded_text = pane.text

    # --- auto-save / run loop -------------------------------------------

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if event.text_area is not self.query_one("#code", TextArea):
            return
        if self.query_one(EditorPane).text == self._loaded_text:
            return
        if self._save_timer is not None:
            self._save_timer.stop()
        self._save_timer = self.set_timer(_DEBOUNCE_SECONDS, self._flush_and_run)

    def _flush_and_run(self) -> None:
        self._save_timer = None
        if self.current is None:
            return
        ex = self._exercise(self.current)
        ex.path.write_text(self.query_one(EditorPane).text, encoding="utf-8")
        self._run_current()

    def _run_current(self) -> None:
        if self.current is None:
            return
        ex = self._exercise(self.current)
        self.run_worker(
            lambda: self._run_blocking(ex), exclusive=True, thread=True
        )

    def _run_blocking(self, exercise: Exercise) -> None:
        result = run_exercise(exercise)
        self.app.call_from_thread(self._apply_result, exercise, result)

    def _apply_result(self, exercise: Exercise, result: RunResult) -> None:
        if exercise.name != self.current:
            return
        self.query_one(OutputPanel).render_result(exercise, result)
        if not result.passed:
            return
        self.app.state.mark_done(exercise.name)
        save_state(self.app.root, self.app.state)
        self.current = next_pending(self._exercises(), self.app.state.completed)
        self._render_state()
        if self.current is None:
            self.query_one(OutputPanel).show_final(
                f"Topic '{self.topic}' complete — press F4 for topics."
            )
            return
        self._load_current()
        self._run_current()

    # --- actions ---------------------------------------------------------

    def action_toggle_hint(self) -> None:
        if self.current is None:
            return
        self.query_one(OutputPanel).toggle_hint(self._exercise(self.current).hint)

    def action_reset(self) -> None:
        from pylings.core.reset import restore

        if self.current is None:
            return
        if self._save_timer is not None:
            self._save_timer.stop()
            self._save_timer = None
        restore(self.app.root, self._exercise(self.current))
        self._load_current()
        self._run_current()

    def action_toggle_list(self) -> None:
        tree = self.query_one(ExerciseTree)
        tree.display = not tree.display

    def action_topics(self) -> None:
        self._flush_pending()
        self.app.pop_screen()

    def action_quit(self) -> None:
        self._flush_pending()
        self.app.exit(0)

    def _flush_pending(self) -> None:
        if self._save_timer is not None:
            self._save_timer.stop()
            self._save_timer = None
            if self.current is not None:
                self._exercise(self.current).path.write_text(
                    self.query_one(EditorPane).text, encoding="utf-8"
                )
