# tests/unit/test_exercise.py

import dataclasses
from pathlib import Path

import pytest

from pylings.core.exercise import Exercise


def _ex(path: Path) -> Exercise:
    return Exercise(
        name="ex", path=path, check_path=path.parent / "check.py", topic="t", hint=""
    )


def test_is_pending_true_when_marker_present(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("# I AM NOT DONE\nprint('hi')\n", encoding="utf-8")
    assert _ex(file).is_pending() is True


def test_is_pending_false_when_marker_removed(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("print('done')\n", encoding="utf-8")
    assert _ex(file).is_pending() is False


def test_is_pending_marker_inside_string_still_counts(tmp_path: Path) -> None:
    # Substring search is intentional — keep it simple, matches rustlings.
    file = tmp_path / "ex.py"
    file.write_text('s = "# I AM NOT DONE"\n', encoding="utf-8")
    assert _ex(file).is_pending() is True


def test_exercise_is_frozen() -> None:
    ex = Exercise(
        name="a",
        path=Path("/tmp/a.py"),
        check_path=Path("/tmp/checks/a.py"),
        topic="t",
        hint="",
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        ex.name = "b"  # type: ignore[misc]


def test_exercise_has_check_path() -> None:
    ex = Exercise(
        name="a",
        path=Path("/tmp/a.py"),
        check_path=Path("/tmp/checks/a.py"),
        topic="t",
        hint="",
    )
    assert ex.check_path == Path("/tmp/checks/a.py")
