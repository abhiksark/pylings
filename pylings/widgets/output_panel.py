# pylings/widgets/output_panel.py
from __future__ import annotations

import os

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from pylings.core.exercise import Exercise, RunResult

_INSTRUCTION = (
    "Press [bold]e[/bold] to open this file in your editor "
    "(or open it yourself), fix the code, and save.\n"
    "This panel re-runs the checks automatically every time you save."
)


class OutputPanel(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("", id="output-header")
        yield Static("Loading…", id="output-body")
        yield Static("", id="hint")

    def render_result(self, exercise: Exercise, result: RunResult) -> None:
        self._render_header(exercise)
        body = self.query_one("#output-body", Static)
        self.remove_class("passed", "failed", "pending")
        if result.timed_out:
            self.add_class("failed")
            body.update(
                "[bold red]Not passing yet[/bold red]\n\n"
                f"Timed out after {result.duration_s:.1f}s — is there an infinite loop?"
            )
            return
        if result.exit_code != 0:
            self.add_class("failed")
            body.update(
                "[bold red]Not passing yet[/bold red]\n\n"
                f"{(result.stderr or result.stdout).rstrip()}"
            )
            return
        if exercise.is_pending():
            self.add_class("pending")
            body.update(
                "[bold yellow]Checks pass![/bold yellow]\n\n"
                "Remove the [yellow]# I AM NOT DONE[/yellow] line from the file "
                "and save again to advance to the next exercise."
            )
            return
        self.add_class("passed")
        body.update(
            f"[bold green]✓ {exercise.name} complete[/bold green]\n\n"
            f"{result.stdout}".rstrip()
        )

    def _render_header(self, exercise: Exercise) -> None:
        header = self.query_one("#output-header", Static)
        header.update(
            f"[bold]{exercise.name}[/bold]   [dim]{self._display_path(exercise)}[/dim]\n"
            f"{_INSTRUCTION}"
        )

    @staticmethod
    def _display_path(exercise: Exercise) -> str:
        # Prefer a short path relative to the working directory; fall back to
        # the absolute path when that isn't possible (e.g. different drives).
        try:
            return os.path.relpath(exercise.path)
        except ValueError:
            return str(exercise.path)

    def toggle_hint(self, text: str) -> None:
        hint = self.query_one("#hint", Static)
        if "visible" in hint.classes:
            hint.remove_class("visible")
        else:
            hint.add_class("visible")
            hint.update(f"[italic]Hint:[/italic] {text or '(no hint provided)'}")
