# pythonlings/core/state.py

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from pythonlings.core.exercise import Exercise

FORMAT_VERSION = 2


@dataclass
class State:
    completed: set[str] = field(default_factory=set)
    seen_intro: bool = False
    last_topic: str | None = None
    last_exercise: str | None = None

    def mark_done(self, name: str) -> None:
        self.completed.add(name)

    def record_resume(self, topic: str, exercise: str | None) -> None:
        self.seen_intro = True
        self.last_topic = topic
        self.last_exercise = exercise

    def clear_resume(self) -> None:
        self.last_topic = None
        self.last_exercise = None


def _state_path(root: Path) -> Path:
    return root / ".pythonlings" / "state.json"


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
        return State(
            completed=set(data.get("completed", [])),
            seen_intro=bool(data.get("seen_intro", False)),
            last_topic=data.get("last_topic"),
            last_exercise=data.get("last_exercise"),
        )
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        backup = path.with_suffix(".json.bak")
        path.rename(backup)
        print(
            f"pythonlings: state file unreadable ({e}); backed up to {backup} "
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
        "seen_intro": state.seen_intro,
        "last_topic": state.last_topic,
        "last_exercise": state.last_exercise,
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
