# pylings/screens/docs.py
from __future__ import annotations

import webbrowser
from urllib.parse import urldefrag

from rich.markup import escape
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Markdown, Static

from pylings.core.docs import load_snippet
from pylings.core.exercise import Exercise


class DocsScreen(ModalScreen[None]):
    """Small in-app reference window for the current exercise."""

    BINDINGS = [
        Binding("escape", "close", "Close", priority=True),
        Binding("o", "open_browser", "Open"),
    ]

    def __init__(self, exercise: Exercise) -> None:
        super().__init__()
        self.exercise = exercise

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(f"[bold]Docs: {escape(self.exercise.name)}[/bold]", id="docs-title"),
            VerticalScroll(
                Markdown(self._reference_markdown(), id="docs-content", open_links=False),
                id="docs-scroll",
            ),
            Static("O Open official docs | Esc Close", id="docs-footer"),
            id="docs-window",
        )

    def action_close(self) -> None:
        self.dismiss()

    def action_open_browser(self) -> None:
        if self.exercise.docs:
            webbrowser.open(self.exercise.docs)

    def _reference_markdown(self) -> str:
        docs = self.exercise.docs or "(no official docs link configured)"
        hint = self.exercise.hint.strip() or "Use this reference while solving."
        snippet = load_snippet(self.exercise.topic, self.exercise.docs)
        if snippet is None:
            local_reference = "No local reference is bundled for this topic."
            snippet_source = ""
        else:
            local_reference = _display_reference(snippet.text)
            snippet_source = snippet.source_url

        source_section = ""
        if snippet_source and _page_url(snippet_source) != _page_url(docs):
            source_section = f"\n\n## Local snippet source\n\n{snippet_source}"

        return (
            f"## Local reference\n\n{local_reference}\n\n"
            f"## Quick note\n\n{hint}\n\n"
            f"## Official Python docs\n\n{docs}{source_section}\n"
        )


def _display_reference(text: str) -> str:
    """Remove file metadata so the modal starts with useful reference text."""
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    lines = _drop_leading_blanks(lines)

    if lines and lines[0].startswith("Source: "):
        lines = lines[1:]
    lines = _drop_leading_blanks(lines)

    if lines and lines[0].startswith("This local reference is generated"):
        lines = lines[1:]
    return "\n".join(_drop_leading_blanks(lines)).strip()


def _drop_leading_blanks(lines: list[str]) -> list[str]:
    while lines and not lines[0].strip():
        lines = lines[1:]
    return lines


def _page_url(url: str) -> str:
    return urldefrag(url).url
