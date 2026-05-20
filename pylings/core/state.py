# pylings/core/state.py

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from pylings.core.exercise import Exercise

FORMAT_VERSION = 2


@dataclass
class State:
    completed: set[str] = field(default_factory=set)

    def mark_done(self, name: str) -> None:
        self.completed.add(name)


def _state_path(root: Path) -> Path:
    return root / ".pylings" / "state.json"


def load(root: Path) -> State:
    path = _state_path(root)
    if not path.exists():
        return State()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("format_version") != FORMAT_VERSION:
            raise ValueError(
                f"unsupported state format_version: {data.get('format_version')}"
            )
        return State(completed=set(data.get("completed", [])))
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        backup = path.with_suffix(".json.bak")
        path.rename(backup)
        print(
            f"pylings: state file unreadable ({e}); backed up to {backup} "
            f"and starting fresh",
            file=sys.stderr,
        )
        return State()


def save(root: Path, state: State) -> None:
    path = _state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "format_version": FORMAT_VERSION,
        "completed": sorted(state.completed),
    }
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)


def next_pending(exercises: list[Exercise], completed: set[str]) -> str | None:
    """First exercise name in `exercises` not in `completed`, or None."""
    for ex in exercises:
        if ex.name not in completed:
            return ex.name
    return None
