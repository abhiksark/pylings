# tests/integration/test_cli_run.py
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


def test_run_passing_exercise_exits_zero() -> None:
    result = _run("--root", str(FIXTURES), "run", "passing")
    assert result.returncode == 0
    assert "passing" in result.stdout


def test_run_failing_exercise_exits_nonzero() -> None:
    result = _run("--root", str(FIXTURES), "run", "asserts")
    assert result.returncode != 0
    assert "AssertionError" in (result.stdout + result.stderr)


def test_run_pending_marker_shows_nudge() -> None:
    result = _run("--root", str(FIXTURES), "run", "pending")
    # exit 0 from the script but the marker blocks pass.
    assert result.returncode != 0
    assert "I AM NOT DONE" in (result.stdout + result.stderr)


def test_run_unknown_exercise_exits_nonzero() -> None:
    result = _run("--root", str(FIXTURES), "run", "nope")
    assert result.returncode != 0
    assert "nope" in result.stderr
