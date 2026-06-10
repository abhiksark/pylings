# pythonlings/core/manifest.py
from __future__ import annotations

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    import tomli as tomllib
from dataclasses import dataclass
from pathlib import Path

from pythonlings.core.exercise import Exercise


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

    def topics(self) -> list[str]:
        """Topic names in first-appearance order."""
        ordered: list[str] = []
        for ex in self.exercises:
            if ex.topic not in ordered:
                ordered.append(ex.topic)
        return ordered

    def exercises_in(self, topic: str) -> list[Exercise]:
        """Exercises belonging to one topic, in curriculum order."""
        return [ex for ex in self.exercises if ex.topic == topic]


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
        if not rel_path.parts or rel_path.parts[0] != "exercises":
            raise ManifestError(
                f"exercise path must be under exercises/: {rel_path}"
            )
        abs_path = root / rel_path
        if not abs_path.exists():
            raise ManifestError(f"exercise path does not exist: {rel_path}")

        # Derive the check path: exercises/<...> mirrors to checks/<...>.
        check_rel = Path("checks", *rel_path.parts[1:])
        check_abs = root / check_rel
        if not check_abs.exists():
            raise ManifestError(f"no check file for {name!r}: {check_rel}")

        exercises.append(
            Exercise(
                name=name,
                path=abs_path,
                check_path=check_abs,
                topic=rel_path.parent.name,
                hint=entry.get("hint", ""),
                docs=entry.get("docs", ""),
                root=root,
                rel_path=rel_path,
                check_rel_path=check_rel,
            )
        )

    return Manifest(
        exercises=exercises,
        welcome_message=data.get("welcome_message", "Welcome to pythonlings!"),
        final_message=data.get("final_message", "All exercises complete."),
    )
