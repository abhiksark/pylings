# pylings/widgets/progress.py
from __future__ import annotations

from textual.widgets import Static

_BAR_WIDTH = 20


def _bar(completed: int, total: int) -> tuple[str, float]:
    pct = (completed / total * 100) if total else 0
    filled = int(_BAR_WIDTH * pct / 100)
    return "█" * filled + "░" * (_BAR_WIDTH - filled), pct


def format_progress(
    completed: int, total: int, overall_completed: int, overall_total: int
) -> str:
    """Render a one-line progress display showing topic and overall progress."""
    topic_bar, topic_pct = _bar(completed, total)
    overall_bar, overall_pct = _bar(overall_completed, overall_total)
    return (
        f"Topic: {topic_bar} {completed}/{total} ({topic_pct:.0f}%)"
        f"   Overall: {overall_bar} {overall_completed}/{overall_total} ({overall_pct:.0f}%)"
    )


class ProgressBar(Static):
    DEFAULT_CSS = ""

    def update_progress(
        self,
        completed: int,
        total: int,
        overall_completed: int,
        overall_total: int,
    ) -> None:
        self.update(
            format_progress(completed, total, overall_completed, overall_total)
        )
