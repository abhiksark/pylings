# pylings/core/manifest.py
from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from pylings.core.exercise import Exercise


class ManifestError(ValueError):
    """info.toml is missing, malformed, or fails validation."""


@dataclass(frozen=True)
class Manifest:
    exercises: list[Exercise]
    welcome_message: str
    final_message: str

    def by_name(self, name: str) -> Exercise:
        for ex in self.exercises:
            if ex.name == name:
                return ex
        raise KeyError(name)

    def index_of(self, name: str) -> int:
        for i, ex in enumerate(self.exercises):
            if ex.name == name:
                return i
        raise KeyError(name)


def load(root: Path) -> Manifest:
    info_path = root / "info.toml"
    if not info_path.exists():
        raise ManifestError(f"info.toml not found at {info_path}")

    with info_path.open("rb") as f:
        data = tomllib.load(f)

    if data.get("format_version") != 1:
        raise ManifestError(
            f"info.toml format_version must be 1, got {data.get('format_version')!r}"
        )

    raw_exercises = data.get("exercises", [])
    if not raw_exercises:
        raise ManifestError("info.toml must define a non-empty [[exercises]] array")

    seen: set[str] = set()
    exercises: list[Exercise] = []
    for entry in raw_exercises:
        name = entry["name"]
        if name in seen:
            raise ManifestError(f"duplicate exercise name: {name!r}")
        seen.add(name)

        rel_path = Path(entry["path"])
        abs_path = root / rel_path
        if not abs_path.exists():
            raise ManifestError(f"exercise path does not exist: {rel_path}")

        exercises.append(
            Exercise(
                name=name,
                path=abs_path,
                topic=rel_path.parent.name,
                hint=entry.get("hint", ""),
            )
        )

    return Manifest(
        exercises=exercises,
        welcome_message=data.get("welcome_message", "Welcome to pylings!"),
        final_message=data.get("final_message", "All exercises complete."),
    )
