# tests/unit/test_runner.py

from pathlib import Path

from pylings.core.exercise import Exercise
from pylings.core.runner import run

CURRICULUM = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"
EXERCISES = CURRICULUM / "exercises"
CHECKS = CURRICULUM / "checks"


def _fixture_ex(name: str) -> Exercise:
    return Exercise(
        name=name,
        path=EXERCISES / f"{name}.py",
        check_path=CHECKS / f"{name}.py",
        topic="t",
        hint="",
    )


def _tmp_ex(tmp_path: Path, exercise_src: str, check_src: str = "") -> Exercise:
    ex_path = tmp_path / "ex.py"
    check_path = tmp_path / "check.py"
    ex_path.write_text(exercise_src, encoding="utf-8")
    check_path.write_text(check_src, encoding="utf-8")
    return Exercise(
        name="ex", path=ex_path, check_path=check_path, topic="t", hint=""
    )


def test_passing_exercise_passes() -> None:
    result = run(_fixture_ex("passing"))
    assert result.passed is True
    assert result.exit_code == 0
    assert "passing" in result.stdout
    assert result.timed_out is False


def test_assertion_error_fails() -> None:
    result = run(_fixture_ex("asserts"))
    assert result.passed is False
    assert result.exit_code != 0
    assert "AssertionError" in result.stderr


def test_syntax_error_fails() -> None:
    result = run(_fixture_ex("syntax"))
    assert result.passed is False
    assert result.exit_code != 0
    assert "SyntaxError" in result.stderr


def test_failing_check_fails_a_clean_exercise(tmp_path: Path) -> None:
    # The exercise runs fine on its own; the hidden check is what fails.
    ex = _tmp_ex(tmp_path, "x = 1\n", "assert x == 2, 'x should be 2'\n")
    result = run(ex)
    assert result.passed is False
    assert "AssertionError" in result.stderr


def test_pending_marker_blocks_pass(tmp_path: Path) -> None:
    # Exit code 0 but the marker is in the exercise file → not passed.
    ex = _tmp_ex(tmp_path, "# I AM NOT DONE\n", "assert True\n")
    result = run(ex)
    assert result.exit_code == 0
    assert result.passed is False


def test_timeout(tmp_path: Path) -> None:
    ex = _tmp_ex(tmp_path, "while True:\n    pass\n")
    result = run(ex, timeout_s=0.5)
    assert result.timed_out is True
    assert result.passed is False


def test_utf8_output(tmp_path: Path) -> None:
    ex = _tmp_ex(tmp_path, "print('héllo 🐍')\n")
    result = run(ex)
    assert result.passed is True
    assert "héllo 🐍" in result.stdout
