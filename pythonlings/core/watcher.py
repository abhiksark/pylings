from __future__ import annotations


def changed_python_file(path: str) -> bool:
    return path.endswith(".py") and "__pycache__" not in path
