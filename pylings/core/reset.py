# pylings/core/reset.py

from __future__ import annotations

import shutil
from pathlib import Path

from pylings.core.exercise import Exercise


class ResetError(RuntimeError):
    """Reset failed (typically: no snapshot exists)."""


def _snapshot_path(root: Path, exercise: Exercise) -> Path:
    return root / ".pylings" / "originals" / exercise.path.name


def snapshot(root: Path, exercise: Exercise) -> None:
    """Copy the pristine source into .pylings/originals/ if not already snapshotted."""
    snap = _snapshot_path(root, exercise)
    if snap.exists():
        return
    snap.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(exercise.path, snap)


def restore(root: Path, exercise: Exercise) -> None:
    """Overwrite the exercise file with its pristine snapshot."""
    snap = _snapshot_path(root, exercise)
    if not snap.exists():
        raise ResetError(
            f"no snapshot for {exercise.name!r}. Has the file been seen by pylings yet?"
        )
    shutil.copy2(snap, exercise.path)
