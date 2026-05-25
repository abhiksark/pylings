# pylings/widgets/output_panel.py
from __future__ import annotations

import os

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from pylings.core.exercise import Exercise, RunResult

_INSTRUCTION = "Edit the code on the left. Checks update automatically."


class OutputPanel(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("", id="output-header")
        yield Static("", id="goal")
        yield Static("", id="docs")
        yield Static("Loading…", id="status")
        yield Static("", id="next-step")
        yield Static("", id="details")
        yield Static("", id="hint")

    def renderable_text(self) -> str:
        parts: list[str] = []
        for widget_id in (
            "output-header",
            "goal",
            "docs",
            "status",
            "next-step",
            "details",
            "hint",
        ):
            parts.append(str(self.query_one(f"#{widget_id}", Static).content))
        return "\n".join(parts)

    def render_running(
        self, exercise: Exercise, completed: int = 0, total: int = 0
    ) -> None:
        self.remove_class("passed", "failed", "pending")
        self._render_header(exercise, completed, total)
        self.query_one("#goal", Static).update(
            f"[bold]Goal[/bold]\n{self._goal_from(exercise)}"
        )
        self._render_docs(exercise)
        self.query_one("#status", Static).update(
            "[bold blue]Running checks...[/bold blue]"
        )
        self.query_one("#next-step", Static).update(
            "Keep editing; results update automatically."
        )
        self.query_one("#details", Static).update("")

    def render_result(
        self,
        exercise: Exercise,
        result: RunResult,
        failures: int = 0,
        completed: int = 0,
        total: int = 0,
    ) -> None:
        self._render_header(exercise, completed, total)
        self.query_one("#goal", Static).update(
            f"[bold]Goal[/bold]\n{self._goal_from(exercise)}"
        )
        self._render_docs(exercise)
        details = (result.stderr or result.stdout).rstrip()
        self.query_one("#details", Static).update(
            f"[bold]Details[/bold]\n{details}" if details else ""
        )
        self.remove_class("passed", "failed", "pending")
        if result.timed_out:
            self.add_class("failed")
            self.query_one("#status", Static).update(
                "[bold red]Not passing yet[/bold red]"
            )
            self.query_one("#next-step", Static).update(
                f"Timed out after {result.duration_s:.1f}s. "
                "Check for an infinite loop."
            )
            return
        if result.exit_code != 0:
            self.add_class("failed")
            self.query_one("#status", Static).update(
                "[bold red]Not passing yet[/bold red]"
            )
            nudge = (
                self._hint_nudge(exercise)
                if failures
                else "Hint available: press F1."
            )
            self.query_one("#next-step", Static).update(
                f"Read the details, fix the code, then pause typing.\n{nudge}"
            )
            return
        if exercise.is_pending():
            self.add_class("pending")
            self.query_one("#status", Static).update(
                "[bold yellow]Checks pass, remove marker[/bold yellow]"
            )
            self.query_one("#next-step", Static).update(
                "Remove the # I AM NOT DONE line to advance."
            )
            return
        self.add_class("passed")
        self.query_one("#status", Static).update(
            f"[bold green]✓ {exercise.name} complete[/bold green]"
        )
        self.query_one("#next-step", Static).update(
            "Loading the next exercise."
        )

    def show_final(self, message: str) -> None:
        """Render the curriculum-complete screen."""
        self.remove_class("failed", "pending")
        self.add_class("passed")
        self.query_one("#hint", Static).remove_class("visible")
        self.query_one("#output-header", Static).update(
            "[bold green]All exercises complete[/bold green]"
        )
        self.query_one("#goal", Static).update("")
        self.query_one("#docs", Static).update("")
        self.query_one("#status", Static).update(message)
        self.query_one("#next-step", Static).update("")
        self.query_one("#details", Static).update("")

    def _render_header(
        self, exercise: Exercise, completed: int = 0, total: int = 0
    ) -> None:
        header = self.query_one("#output-header", Static)
        progress = f"   [dim]{completed}/{total} complete[/dim]" if total else ""
        header.update(
            f"[bold]{exercise.name}[/bold]{progress}   "
            f"[dim]{self._display_path(exercise)}[/dim]\n"
            f"{_INSTRUCTION}"
        )

    def _goal_from(self, exercise: Exercise) -> str:
        for line in exercise.path.read_text(encoding="utf-8").splitlines()[:12]:
            stripped = line.strip()
            if stripped.startswith("# Goal:"):
                return stripped.removeprefix("# Goal:").strip()
            if stripped.startswith("# Exercise:"):
                return stripped.removeprefix("# Exercise:").strip()
        return exercise.name

    def _render_docs(self, exercise: Exercise) -> None:
        docs = exercise.docs.strip()
        self.query_one("#docs", Static).update(
            f"[bold]Docs[/bold]\n{docs}" if docs else ""
        )

    @staticmethod
    def _hint_nudge(exercise: Exercise) -> str:
        first = exercise.hint.strip().split(".")[0].strip()
        return f"{first}." if first else "Hint available: press F1."

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

    def reset_hint(self) -> None:
        hint = self.query_one("#hint", Static)
        hint.remove_class("visible")
        hint.update("")
