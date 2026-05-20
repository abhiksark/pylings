# pylings/app.py
from __future__ import annotations

import asyncio
import os
import shlex
import subprocess
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import Footer, Header

from pylings.core.manifest import Manifest, load as load_manifest
from pylings.core.runner import run as run_exercise
from pylings.core.state import State, load as load_state, save as save_state
from pylings.core.watcher import watch
from pylings.widgets.exercise_tree import ExerciseTree
from pylings.widgets.output_panel import OutputPanel
from pylings.widgets.progress import ProgressBar


class PylingsApp(App[int]):
    CSS_PATH = "pylings.tcss"
    BINDINGS = [
        Binding("e", "edit", "Edit"),
        Binding("h", "toggle_hint", "Hint"),
        Binding("r", "reset", "Reset"),
        Binding("n", "skip_animation", "Next"),
        Binding("l", "toggle_list", "List"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, root: Path) -> None:
        super().__init__()
        self.root = root
        self.manifest: Manifest = load_manifest(root)
        self.state: State = load_state(root)
        if self.state.current is None:
            self.state.current = self.state.next_pending(self.manifest)
        self._watcher_task: asyncio.Task[None] | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield ProgressBar(id="progress")
        yield Horizontal(ExerciseTree(), OutputPanel(id="output"), id="main")
        yield Footer()

    async def on_mount(self) -> None:
        self.title = "pylings"
        self.sub_title = self.manifest.welcome_message
        self._render_state()
        await self._run_current()
        self._restart_watcher()

    def _render_state(self) -> None:
        tree = self.query_one(ExerciseTree)
        tree.render_manifest(self.manifest, self.state)
        progress = self.query_one(ProgressBar)
        progress.update_progress(len(self.state.completed), len(self.manifest.exercises))

    async def _run_current(self) -> None:
        if self.state.current is None:
            self.exit(0)
            return
        ex = self.manifest.by_name(self.state.current)
        result = run_exercise(ex)
        self.query_one(OutputPanel).render_result(ex, result)
        if result.passed:
            self.state.mark_done(ex.name, self.manifest)
            save_state(self.root, self.state)
            self._render_state()
            self._restart_watcher()

    def _restart_watcher(self) -> None:
        if self._watcher_task is not None:
            self._watcher_task.cancel()
        if self.state.current is None:
            return
        ex = self.manifest.by_name(self.state.current)
        self._watcher_task = asyncio.create_task(self._watch_loop(ex.path))

    async def _watch_loop(self, path: Path) -> None:
        async for _ in watch(path):
            await self._run_current()

    def action_toggle_hint(self) -> None:
        if self.state.current is None:
            return
        ex = self.manifest.by_name(self.state.current)
        self.query_one(OutputPanel).toggle_hint(ex.hint)

    def action_reset(self) -> None:
        from pylings.core.reset import restore

        if self.state.current is None:
            return
        ex = self.manifest.by_name(self.state.current)
        restore(self.root, ex)
        # Resetting the current exercise: state is unchanged (per spec), file is
        # rewritten. Re-run explicitly because shutil.copy may not trip the
        # watcher's mtime threshold on every platform.
        save_state(self.root, self.state)
        asyncio.create_task(self._run_current())

    @staticmethod
    def _resolve_editor() -> list[str] | None:
        """Return the editor command (split into argv) from $VISUAL/$EDITOR."""
        raw = os.environ.get("VISUAL") or os.environ.get("EDITOR")
        if not raw:
            return None
        return shlex.split(raw)

    def action_edit(self) -> None:
        if self.state.current is None:
            return
        ex = self.manifest.by_name(self.state.current)
        editor = self._resolve_editor()
        if editor is None:
            self.notify(
                f"No $EDITOR set — open {ex.path} yourself, or export EDITOR.",
                severity="warning",
                timeout=6,
            )
            return
        try:
            with self.suspend():
                subprocess.run([*editor, str(ex.path)])
        except Exception as exc:  # editor missing, suspend unsupported, etc.
            self.notify(f"Could not open editor: {exc}", severity="error", timeout=6)
            return
        # Re-run: the watcher was paused while the TUI was suspended, so a save
        # made inside the editor would otherwise go unnoticed until the next one.
        asyncio.create_task(self._run_current())

    def action_skip_animation(self) -> None:
        # Reserved for the success animation; for now a no-op outside that window.
        pass

    def action_toggle_list(self) -> None:
        tree = self.query_one(ExerciseTree)
        tree.display = not tree.display


def run_tui(root: Path) -> int:
    return PylingsApp(root).run() or 0
