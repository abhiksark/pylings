# tests/unit/test_reset.py

from pathlib import Path

import pytest

from pylings.core.exercise import Exercise
from pylings.core.reset import ResetError, restore, snapshot


def _ex(tmp_path: Path, contents: str) -> Exercise:
    file = tmp_path / "ex.py"
    file.write_text(contents, encoding="utf-8")
    return Exercise(name="ex", path=file, topic="t", hint="")


def test_snapshot_copies_file_to_pylings_originals(tmp_path: Path) -> None:
    ex = _ex(tmp_path, "original content\n")
    snapshot(tmp_path, ex)
    snap = tmp_path / ".pylings" / "originals" / "ex.py"
    assert snap.exists()
    assert snap.read_text() == "original content\n"


def test_snapshot_does_not_overwrite_existing(tmp_path: Path) -> None:
    ex = _ex(tmp_path, "first\n")
    snapshot(tmp_path, ex)
    ex.path.write_text("modified\n", encoding="utf-8")
    snapshot(tmp_path, ex)  # second call should be a no-op
    snap = tmp_path / ".pylings" / "originals" / "ex.py"
    assert snap.read_text() == "first\n"


def test_restore_writes_snapshot_back_to_exercise(tmp_path: Path) -> None:
    ex = _ex(tmp_path, "pristine\n")
    snapshot(tmp_path, ex)
    ex.path.write_text("learner edits\n", encoding="utf-8")

    restore(tmp_path, ex)
    assert ex.path.read_text() == "pristine\n"


def test_restore_raises_when_no_snapshot(tmp_path: Path) -> None:
    ex = _ex(tmp_path, "no snapshot taken")
    with pytest.raises(ResetError, match="snapshot"):
        restore(tmp_path, ex)
