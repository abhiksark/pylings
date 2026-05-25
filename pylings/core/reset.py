# pylings/core/reset.py

from __future__ import annotations

import shutil
from pathlib import Path

from pylings.core.exercise import Exercise


class ResetError(RuntimeError):
    """Reset failed (typically: no snapshot exists)."""


def _snapshot_path(root: Path, exercise: Exercise) -> Path:
    # Key on Exercise.name (unique per the manifest validator) so two
    # exercises in different topics with the same filename don't collide.
    return root / ".pylings" / "originals" / f"{exercise.name}.py"


def _original_path(root: Path, exercise: Exercise) -> Path:
    if exercise.rel_path is None:
        return _snapshot_path(root, exercise)
    return root / ".pylings" / "originals" / exercise.rel_path.relative_to("exercises")


def snapshot(root: Path, exercise: Exercise) -> None:
    """Copy the pristine source into .pylings/originals/ if not already snapshotted."""
    snap = _original_path(root, exercise)
    if snap.exists():
        return
    snap.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(exercise.path, snap)


def restore(root: Path, exercise: Exercise) -> None:
    """Overwrite the exercise file with its pristine original."""
    snap = _original_path(root, exercise)
    if not snap.exists():
        raise ResetError(
            f"no snapshot for {exercise.name!r}. Run 'pylings update' first."
        )
    shutil.copy2(snap, exercise.path)
