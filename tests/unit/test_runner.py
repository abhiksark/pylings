# tests/unit/test_runner.py

from pathlib import Path

from pylings.core.exercise import Exercise
from pylings.core.runner import run

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum" / "exercises"


def _ex(name: str, path: Path) -> Exercise:
    return Exercise(name=name, path=path, topic="t", hint="")


def test_passing_exercise_passes() -> None:
    result = run(_ex("passing", FIXTURES / "passing.py"))
    assert result.passed is True
    assert result.exit_code == 0
    assert result.stdout.startswith("passing")
    assert result.timed_out is False


def test_assertion_error_fails() -> None:
    result = run(_ex("asserts", FIXTURES / "asserts.py"))
    assert result.passed is False
    assert result.exit_code != 0
    assert "AssertionError" in result.stderr


def test_syntax_error_fails() -> None:
    result = run(_ex("syntax", FIXTURES / "syntax.py"))
    assert result.passed is False
    assert result.exit_code != 0
    assert "SyntaxError" in result.stderr


def test_pending_marker_blocks_pass(tmp_path: Path) -> None:
    # Exit code 0 but marker present → not passed.
    file = tmp_path / "ex.py"
    file.write_text("# I AM NOT DONE\nassert True\n", encoding="utf-8")
    result = run(_ex("ex", file))
    assert result.exit_code == 0
    assert result.passed is False


def test_timeout(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("while True:\n    pass\n", encoding="utf-8")
    result = run(_ex("ex", file), timeout_s=0.5)
    assert result.timed_out is True
    assert result.passed is False


def test_utf8_output(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("print('héllo 🐍')\n", encoding="utf-8")
    result = run(_ex("ex", file))
    assert result.passed is True
    assert "héllo 🐍" in result.stdout
