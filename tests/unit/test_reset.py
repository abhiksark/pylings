# tests/unit/test_reset.py

from pathlib import Path

import pytest

from pylings.core.curriculum import init_workspace
from pylings.core.exercise import Exercise
from pylings.core.manifest import load
from pylings.core.reset import ResetError, restore, snapshot


def _ex(tmp_path: Path, contents: str) -> Exercise:
    file = tmp_path / "ex.py"
    file.write_text(contents, encoding="utf-8")
    return Exercise(
        name="ex",
        path=file,
        check_path=tmp_path / "check.py",
        topic="t",
        hint="",
    )


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


def test_snapshot_keys_on_exercise_name_not_filename(tmp_path: Path) -> None:
    # Two exercises with the same filename in different topic subdirs must
    # snapshot to distinct files (regression: previously keyed on
    # path.name, causing silent collision).
    (tmp_path / "exercises" / "variables").mkdir(parents=True)
    (tmp_path / "exercises" / "functions").mkdir(parents=True)

    a_path = tmp_path / "exercises" / "variables" / "utils.py"
    b_path = tmp_path / "exercises" / "functions" / "utils.py"
    a_path.write_text("variables-version\n", encoding="utf-8")
    b_path.write_text("functions-version\n", encoding="utf-8")

    a = Exercise(
        name="variables_utils",
        path=a_path,
        check_path=tmp_path / "checks" / "variables_utils.py",
        topic="variables",
        hint="",
    )
    b = Exercise(
        name="functions_utils",
        path=b_path,
        check_path=tmp_path / "checks" / "functions_utils.py",
        topic="functions",
        hint="",
    )

    snapshot(tmp_path, a)
    snapshot(tmp_path, b)

    originals = tmp_path / ".pylings" / "originals"
    assert (originals / "variables_utils.py").read_text() == "variables-version\n"
    assert (originals / "functions_utils.py").read_text() == "functions-version\n"


def test_restore_uses_pristine_originals_not_current_file(tmp_path: Path) -> None:
    root = init_workspace(tmp_path / "workspace")
    manifest = load(root)
    exercise = manifest.exercises[0]
    original = root / ".pylings" / "originals" / exercise.rel_path.relative_to(
        "exercises"
    )
    pristine = original.read_text(encoding="utf-8")
    exercise.path.write_text("# corrupted user edit\n", encoding="utf-8")

    restore(root, exercise)

    assert exercise.path.read_text(encoding="utf-8") == pristine
