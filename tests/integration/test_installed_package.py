from pathlib import Path

from pythonlings.cli import main


def test_package_can_initialize_and_list_workspace(tmp_path: Path) -> None:
    root = tmp_path / "workspace"

    assert main(["init", "--path", str(root)]) == 0
    assert main(["--root", str(root), "list"]) == 0
    assert (root / "solutions" / "_answers.py").exists()
