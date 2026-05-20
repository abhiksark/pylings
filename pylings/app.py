# pylings/app.py
from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.timer import Timer
from textual.widgets import Footer, Header, TextArea

from pylings.core.exercise import Exercise, RunResult
from pylings.core.manifest import Manifest, load as load_manifest
from pylings.core.runner import run as run_exercise
from pylings.core.state import State, load as load_state, save as save_state, next_pending
from pylings.widgets.editor_pane import EditorPane
from pylings.widgets.exercise_tree import ExerciseTree
from pylings.widgets.output_panel import OutputPanel
from pylings.widgets.progress import ProgressBar

_DEBOUNCE_SECONDS = 0.6


class PylingsApp(App[int]):
    CSS_PATH = "pylings.tcss"
    BINDINGS = [
        Binding("f1", "toggle_hint", "Hint"),
        Binding("f2", "reset", "Reset"),
        Binding("f3", "toggle_list", "List"),
        Binding("ctrl+q", "quit", "Quit"),
    ]

    def __init__(self, root: Path) -> None:
        super().__init__()
        self.root = root
        self.manifest: Manifest = load_manifest(root)
        self.state: State = load_state(root)
        self.current: str | None = next_pending(
            self.manifest.exercises, self.state.completed
        )
        self._save_timer: Timer | None = None
        # The editor content as last loaded from disk. Used to tell a real
        # edit apart from the Changed event that a programmatic load emits.
        self._loaded_text = ""

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
        self.title = "pylings"
        self.sub_title = self.manifest.welcome_message
        self._render_state()
        if self.current is None:
            # The curriculum was already complete when pylings launched.
            self.query_one(OutputPanel).show_final(self.manifest.final_message)
            return
        self._load_current()
        self._run_current()
        self.query_one(EditorPane).focus_editor()

    # --- rendering -------------------------------------------------------

    def _render_state(self) -> None:
        self.query_one(ExerciseTree).render_manifest(self.manifest, self.state, self.current)
        self.query_one(ProgressBar).update_progress(
            len(self.state.completed), len(self.manifest.exercises)
        )

    def _load_current(self) -> None:
        """Load the current exercise file into the editor (no run)."""
        if self.current is None:
            return
        if self._save_timer is not None:
            self._save_timer.stop()
            self._save_timer = None
        exercise = self.manifest.by_name(self.current)
        pane = self.query_one(EditorPane)
        pane.load_exercise(exercise)
        self._loaded_text = pane.text

    # --- the auto-save / run loop ---------------------------------------

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if event.text_area is not self.query_one("#code", TextArea):
            return
        # Ignore the Changed event emitted by a programmatic load, and any
        # edit that lands the buffer back on the loaded baseline.
        if self.query_one(EditorPane).text == self._loaded_text:
            return
        if self._save_timer is not None:
            self._save_timer.stop()
        self._save_timer = self.set_timer(_DEBOUNCE_SECONDS, self._flush_and_run)

    def _flush_and_run(self) -> None:
        self._save_timer = None
        if self.current is None:
            return
        exercise = self.manifest.by_name(self.current)
        exercise.path.write_text(self.query_one(EditorPane).text, encoding="utf-8")
        self._run_current()

    def _run_current(self) -> None:
        if self.current is None:
            return
        exercise = self.manifest.by_name(self.current)
        self.run_worker(
            lambda: self._run_blocking(exercise), exclusive=True, thread=True
        )

    def _run_blocking(self, exercise: Exercise) -> None:
        # Runs on a worker thread; never touches widgets directly.
        result = run_exercise(exercise)
        self.call_from_thread(self._apply_result, exercise, result)

    def _apply_result(self, exercise: Exercise, result: RunResult) -> None:
        if exercise.name != self.current:
            return  # a superseded run finished late — ignore its result
        self.query_one(OutputPanel).render_result(exercise, result)
        if not result.passed:
            return
        self.state.mark_done(exercise.name)
        self.current = next_pending(self.manifest.exercises, self.state.completed)
        save_state(self.root, self.state)
        self._render_state()
        if self.current is None:
            self.query_one(OutputPanel).show_final(self.manifest.final_message)
            return
        self._load_current()
        self._run_current()

    # --- actions ---------------------------------------------------------

    def action_toggle_hint(self) -> None:
        if self.current is None:
            return
        exercise = self.manifest.by_name(self.current)
        self.query_one(OutputPanel).toggle_hint(exercise.hint)

    def action_reset(self) -> None:
        from pylings.core.reset import restore

        if self.current is None:
            return
        if self._save_timer is not None:
            self._save_timer.stop()
            self._save_timer = None
        exercise = self.manifest.by_name(self.current)
        restore(self.root, exercise)
        self._load_current()
        self._run_current()

    def action_toggle_list(self) -> None:
        tree = self.query_one(ExerciseTree)
        tree.display = not tree.display

    def action_quit(self) -> None:
        # Flush a pending edit so the last keystrokes aren't lost on quit.
        if self._save_timer is not None:
            self._save_timer.stop()
            self._save_timer = None
            if self.current is not None:
                exercise = self.manifest.by_name(self.current)
                exercise.path.write_text(
                    self.query_one(EditorPane).text, encoding="utf-8"
                )
        self.exit(0)


def run_tui(root: Path, start_topic: str | None = None) -> int:
    return PylingsApp(root).run() or 0
