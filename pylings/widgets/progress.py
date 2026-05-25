# pylings/widgets/progress.py
from __future__ import annotations

from textual.widgets import Static


class ProgressBar(Static):
    DEFAULT_CSS = ""

    def update_progress(self, completed: int, total: int) -> None:
        pct = (completed / total * 100) if total else 0
        bar_width = 20
        filled = int(bar_width * pct / 100)
        bar = "█" * filled + "░" * (bar_width - filled)
        self.update(f"Progress: {bar}  {completed}/{total}  ({pct:.0f}%)")
