# tests/integration/test_cli_reset.py
import shutil
import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _run(*args: str, input: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pylings", *args],
        capture_output=True,
        text=True,
        input=input,
    )


def test_reset_restores_pristine_content_with_yes(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work, ignore=shutil.ignore_patterns(".pylings"))
    target = work / "exercises" / "passing.py"
    original = target.read_text()

    # Take a snapshot (verify implicitly snapshots through state-aware code;
    # for reset, we explicitly run verify first to populate originals/).
    _run("--root", str(work), "list")  # any command that triggers snapshot

    target.write_text("# scrambled by learner\n", encoding="utf-8")
    result = _run("--root", str(work), "reset", "passing", "--yes")
    assert result.returncode == 0
    assert target.read_text() == original


def test_reset_without_yes_aborts_on_no(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work, ignore=shutil.ignore_patterns(".pylings"))
    _run("--root", str(work), "list")
    target = work / "exercises" / "passing.py"
    target.write_text("scrambled", encoding="utf-8")

    result = _run("--root", str(work), "reset", "passing", input="n\n")
    assert result.returncode == 0
    assert target.read_text() == "scrambled"


def test_reset_unknown_exercise_exits_nonzero() -> None:
    result = _run("--root", str(FIXTURES), "reset", "nope", "--yes")
    assert result.returncode != 0


