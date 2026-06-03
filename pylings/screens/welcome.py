# pylings/screens/welcome.py
from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Static

from pylings.core.state import save as save_state


def welcome_text() -> str:
    """The first-launch explainer for the edit/save/advance loop."""
    return (
        "You learn Python here by fixing small broken programs. The loop is:\n\n"
        "  1. Open the current exercise file in your own editor.\n"
        "  2. Fix the code and save -- the check reruns automatically.\n"
        "  3. Remove the `# I AM NOT DONE` marker to advance to the next one.\n\n"
        "Handy keys: F1 hint - F3 exercise list - F4 topics - "
        "F5 local docs - Ctrl+Q quit.\n\n"
        "Press Enter to start."
    )


class WelcomeScreen(ModalScreen[None]):
    """First-launch onboarding overlay explaining the core loop."""

    BINDINGS = [
        Binding("enter", "start", "Start", priority=True),
        Binding("escape", "start", "Start"),
    ]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("[bold]Welcome to pylings[/bold]", id="welcome-title"),
            Static(welcome_text(), id="welcome-body"),
            Static("Enter  Start", id="welcome-footer"),
            id="welcome-window",
        )

    def action_start(self) -> None:
        self.app.state.seen_intro = True
        save_state(self.app.root, self.app.state)
        self.dismiss()
