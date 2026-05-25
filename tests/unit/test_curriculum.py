from pathlib import Path

from pylings.core import curriculum


def test_source_root_finds_curriculum_files() -> None:
    root = curriculum.source_root()

    assert (root / "info.toml").exists()
    assert (root / "exercises").is_dir()
    assert (root / "checks").is_dir()


def test_init_workspace_copies_curriculum(tmp_path: Path) -> None:
    target = tmp_path / "workspace"

    result = curriculum.init_workspace(target)

    assert result == target.resolve()
    assert (target / "info.toml").exists()
    assert (target / "exercises").is_dir()
    assert (target / "checks").is_dir()
    assert (target / "solutions").is_dir()
    assert (target / ".pylings" / "originals").is_dir()
    assert (target / ".gitignore").read_text(encoding="utf-8").splitlines() == [
        ".pylings/state.json",
        ".pylings_debug.log",
        "__pycache__/",
        "*.pyc",
    ]


def test_init_workspace_refuses_non_empty_directory(tmp_path: Path) -> None:
    target = tmp_path / "workspace"
    target.mkdir()
    (target / "notes.txt").write_text("keep me", encoding="utf-8")

    try:
        curriculum.init_workspace(target)
    except curriculum.WorkspaceError as exc:
        assert "already exists and is not empty" in str(exc)
    else:
        raise AssertionError("expected WorkspaceError")


def test_update_workspace_preserves_user_exercise_edit(tmp_path: Path) -> None:
    target = curriculum.init_workspace(tmp_path / "workspace")
    exercise = next((target / "exercises").rglob("*.py"))
    exercise.write_text("# user edit\n", encoding="utf-8")

    curriculum.update_workspace(target)

    assert exercise.read_text(encoding="utf-8") == "# user edit\n"
    original = target / ".pylings" / "originals" / exercise.relative_to(target / "exercises")
    assert original.exists()
    assert (target / "solutions" / "_answers.py").exists()
