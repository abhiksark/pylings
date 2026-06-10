from pathlib import Path

from pythonlings.cli import main


def test_solution_command_runs_workspace_solution(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    (root / "solutions").mkdir(parents=True)
    (root / "checks").mkdir()
    (root / "exercises").mkdir()
    (root / "info.toml").write_text(
        """
format_version = 1

[[exercises]]
name = "passing1"
path = "exercises/passing1.py"
hint = "set x"
docs = "https://docs.python.org/3/"
""",
        encoding="utf-8",
    )
    (root / "exercises" / "passing1.py").write_text("x = 0\n", encoding="utf-8")
    (root / "solutions" / "passing1.py").write_text("x = 1\n", encoding="utf-8")
    (root / "checks" / "passing1.py").write_text("assert x == 1\n", encoding="utf-8")

    code = main(["--root", str(root), "solution", "passing1"])

    assert code == 0


def test_debug_writes_workspace_log(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    (root / "checks").mkdir(parents=True)
    (root / "exercises").mkdir()
    (root / "info.toml").write_text(
        """
format_version = 1

[[exercises]]
name = "passing1"
path = "exercises/passing1.py"
hint = "set x"
docs = "https://docs.python.org/3/"
""",
        encoding="utf-8",
    )
    (root / "exercises" / "passing1.py").write_text("x = 1\n", encoding="utf-8")
    (root / "checks" / "passing1.py").write_text("assert x == 1\n", encoding="utf-8")

    code = main(["--debug", "--root", str(root), "run", "passing1"])

    assert code == 0
    assert "run" in (root / ".pythonlings_debug.log").read_text(encoding="utf-8")
