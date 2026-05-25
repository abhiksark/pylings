from pylings.core.watcher import changed_python_file


def test_changed_python_file_accepts_exercise_file() -> None:
    assert changed_python_file("exercises/variables/variables1.py") is True


def test_changed_python_file_ignores_bytecode() -> None:
    assert changed_python_file("exercises/variables/__pycache__/variables1.pyc") is False


def test_changed_python_file_ignores_non_python_files() -> None:
    assert changed_python_file("Readme.md") is False
