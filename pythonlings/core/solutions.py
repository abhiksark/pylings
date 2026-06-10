from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from pythonlings.core.exercise import Exercise


class SolutionError(RuntimeError):
    """Solution lookup failed."""


def solution_exercise(root: Path, exercise: Exercise) -> Exercise:
    path = root / "solutions" / f"{exercise.name}.py"
    if not path.exists():
        raise SolutionError(f"no solution for {exercise.name!r}")
    return replace(exercise, path=path, rel_path=Path("solutions") / path.name)
