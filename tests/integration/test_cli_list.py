# tests/integration/test_cli_list.py
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


def test_list_shows_all_exercises_in_order(tmp_path: Path, monkeypatch) -> None:
    # Use a copy of the fixture so we can control state without polluting it.
    import shutil
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work, ignore=shutil.ignore_patterns(".pylings"))

    result = _run("--root", str(work), "list")
    assert result.returncode == 0
    lines = [l for l in result.stdout.splitlines() if l.strip()]
    # Each line ends in "<topic>/<name>"; extract the name segment.
    names = [l.split()[-1].split("/")[-1] for l in lines]
    assert names == ["passing", "asserts", "syntax", "pending"]
    # Topic prefix should be present for every line.
    assert all("exercises/" in line for line in lines)


def test_list_marks_current_with_dot(tmp_path: Path) -> None:
    import shutil
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work, ignore=shutil.ignore_patterns(".pylings"))
    result = _run("--root", str(work), "list")
    # First exercise should be marked as current on a fresh state.
    first_line = next(l for l in result.stdout.splitlines() if "passing" in l)
    assert "●" in first_line
