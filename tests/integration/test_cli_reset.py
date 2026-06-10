# tests/integration/test_cli_reset.py
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from pythonlings.core.curriculum import init_workspace

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _run(*args: str, input: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pythonlings", *args],
        capture_output=True,
        text=True,
        input=input,
    )


def test_reset_restores_pristine_content_with_yes(tmp_path: Path) -> None:
    work = init_workspace(tmp_path / "work")
    target = next((work / "exercises").rglob("variables1.py"))
    original = target.read_text()

    target.write_text("# scrambled by learner\n", encoding="utf-8")
    result = _run("--root", str(work), "reset", "variables1", "--yes")
    assert result.returncode == 0
    assert target.read_text() == original


def test_reset_without_yes_aborts_on_no(tmp_path: Path) -> None:
    work = init_workspace(tmp_path / "work")
    target = next((work / "exercises").rglob("variables1.py"))
    target.write_text("scrambled", encoding="utf-8")

    result = _run("--root", str(work), "reset", "variables1", input="n\n")
    assert result.returncode == 0
    assert target.read_text() == "scrambled"


def test_reset_does_not_create_original_from_current_file(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work, ignore=shutil.ignore_patterns(".pythonlings"))
    target = work / "exercises" / "passing.py"
    target.write_text("# learner edit before reset\n", encoding="utf-8")

    result = _run("--root", str(work), "reset", "passing", "--yes")

    assert result.returncode != 0
    assert "Run 'pythonlings update' first" in result.stderr
    assert target.read_text() == "# learner edit before reset\n"


def test_reset_unknown_exercise_exits_nonzero() -> None:
    result = _run("--root", str(FIXTURES), "reset", "nope", "--yes")
    assert result.returncode != 0

