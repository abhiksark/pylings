# tests/integration/test_cli_hint.py
import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pylings", *args],
        capture_output=True,
        text=True,
    )


def test_hint_prints_text_for_known_exercise() -> None:
    result = _run("--root", str(FIXTURES), "hint", "asserts")
    assert result.returncode == 0
    assert "AssertionError" in result.stdout
    assert "https://docs.python.org/3/tutorial/errors.html" in result.stdout


def test_hint_for_unknown_exercise_exits_nonzero() -> None:
    result = _run("--root", str(FIXTURES), "hint", "nope")
    assert result.returncode != 0
    assert "nope" in result.stderr
