# pylings/widgets/output_panel.py
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from pylings.core.exercise import Exercise, RunResult


class OutputPanel(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("(no run yet)", id="output-body")
        yield Static("", id="hint")

    def render_result(self, exercise: Exercise, result: RunResult) -> None:
        body = self.query_one("#output-body", Static)
        self.remove_class("passed", "failed", "pending")
        if result.timed_out:
            self.add_class("failed")
            body.update(f"[bold]Timed out after {result.duration_s:.1f}s[/bold] — possible infinite loop?")
            return
        if result.exit_code != 0:
            self.add_class("failed")
            body.update(f"[bold red]FAIL[/bold red]\n{result.stderr or result.stdout}")
            return
        if exercise.is_pending():
            self.add_class("pending")
            body.update(
                "[bold]Tests pass![/bold] Remove the [yellow]# I AM NOT DONE[/yellow] line to advance."
            )
            return
        self.add_class("passed")
        body.update(f"[bold green]✓ {exercise.name}[/bold green]\n{result.stdout}")

    def toggle_hint(self, text: str) -> None:
        hint = self.query_one("#hint", Static)
        if "visible" in hint.classes:
            hint.remove_class("visible")
        else:
            hint.add_class("visible")
            hint.update(f"[italic]Hint:[/italic] {text or '(no hint provided)'}")
