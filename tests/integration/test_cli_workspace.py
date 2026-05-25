from pathlib import Path

from pylings.cli import main


def test_init_command_creates_workspace(tmp_path: Path) -> None:
    target = tmp_path / "learn-python"

    code = main(["init", "--path", str(target)])

    assert code == 0
    assert (target / "info.toml").exists()
    assert (target / "exercises").is_dir()
    assert (target / "checks").is_dir()


def test_init_command_requires_force_for_non_empty_directory(
    tmp_path: Path, capsys
) -> None:
    target = tmp_path / "learn-python"
    target.mkdir()
    (target / "notes.txt").write_text("keep", encoding="utf-8")

    code = main(["init", "--path", str(target)])

    assert code == 1
    assert "already exists and is not empty" in capsys.readouterr().err


def test_update_command_preserves_user_exercises(tmp_path: Path) -> None:
    target = tmp_path / "learn-python"
    assert main(["init", "--path", str(target)]) == 0
    exercise = next((target / "exercises").rglob("*.py"))
    exercise.write_text("# edited\n", encoding="utf-8")

    code = main(["update", "--path", str(target)])

    assert code == 0
    assert exercise.read_text(encoding="utf-8") == "# edited\n"
    assert (target / ".pylings" / "originals").is_dir()
