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
    shutil.copytree(FIXTURES, work)
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
    shutil.copytree(FIXTURES, work)
    _run("--root", str(work), "list")
    target = work / "exercises" / "passing.py"
    target.write_text("scrambled", encoding="utf-8")

    result = _run("--root", str(work), "reset", "passing", input="n\n")
    assert result.returncode == 0
    assert target.read_text() == "scrambled"


def test_reset_unknown_exercise_exits_nonzero() -> None:
    result = _run("--root", str(FIXTURES), "reset", "nope", "--yes")
    assert result.returncode != 0


def test_reset_rewinds_state_when_target_precedes_current(tmp_path: Path) -> None:
    """If you reset an exercise that's already completed and earlier than
    the current cursor, state should rewind: completed -= {name} and
    current = name."""
    import json

    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    _run("--root", str(work), "list")  # snapshot

    # Hand-craft state: completed=[passing, asserts], current=syntax.
    state_dir = work / ".pylings"
    state_dir.mkdir(exist_ok=True)
    (state_dir / "state.json").write_text(
        json.dumps({
            "format_version": 1,
            "completed": ["passing", "asserts"],
            "current": "syntax",
        }),
        encoding="utf-8",
    )

    result = _run("--root", str(work), "reset", "passing", "--yes")
    assert result.returncode == 0
    state = json.loads((state_dir / "state.json").read_text())
    assert "passing" not in state["completed"]
    assert state["current"] == "passing"


def test_reset_leaves_state_unchanged_when_target_is_current(tmp_path: Path) -> None:
    import json

    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    _run("--root", str(work), "list")

    state_dir = work / ".pylings"
    state_dir.mkdir(exist_ok=True)
    (state_dir / "state.json").write_text(
        json.dumps({
            "format_version": 1,
            "completed": [],
            "current": "passing",
        }),
        encoding="utf-8",
    )

    result = _run("--root", str(work), "reset", "passing", "--yes")
    assert result.returncode == 0
    state = json.loads((state_dir / "state.json").read_text())
    assert state["completed"] == []
    assert state["current"] == "passing"
