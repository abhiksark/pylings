from __future__ import annotations

import shutil
from importlib import resources
from pathlib import Path


class WorkspaceError(RuntimeError):
    """Workspace init or update failed."""


CURRICULUM_DIRS = ("exercises", "checks", "solutions")
GITIGNORE_LINES = [
    ".pylings/state.json",
    ".pylings_debug.log",
    "__pycache__/",
    "*.pyc",
]


def source_root() -> Path:
    """Return the curriculum source root for editable and wheel installs."""
    packaged = resources.files("pylings").joinpath("curriculum")
    if packaged.joinpath("info.toml").is_file():
        return Path(str(packaged))

    repo_root = Path(__file__).resolve().parents[2]
    if (repo_root / "info.toml").exists():
        return repo_root

    raise WorkspaceError("packaged curriculum not found")


def _copy_path(src: Path, dst: Path, *, overwrite: bool) -> None:
    if src.is_dir():
        if dst.exists() and overwrite:
            shutil.rmtree(dst)
        dst.mkdir(parents=True, exist_ok=True)
        for child in src.iterdir():
            _copy_path(child, dst / child.name, overwrite=overwrite)
        return

    if dst.exists() and not overwrite:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _write_workspace_gitignore(root: Path) -> None:
    (root / ".gitignore").write_text(
        "\n".join(GITIGNORE_LINES) + "\n",
        encoding="utf-8",
    )


def _sync_originals(root: Path, src_root: Path) -> None:
    originals = root / ".pylings" / "originals"
    if originals.exists():
        shutil.rmtree(originals)
    for exercise in (src_root / "exercises").rglob("*.py"):
        rel = exercise.relative_to(src_root / "exercises")
        target = originals / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(exercise, target)


def init_workspace(path: Path, *, force: bool = False) -> Path:
    path = path.expanduser().resolve()
    if path.exists() and any(path.iterdir()) and not force:
        raise WorkspaceError(f"{path} already exists and is not empty")
    path.mkdir(parents=True, exist_ok=True)

    src_root = source_root()
    _copy_path(src_root / "info.toml", path / "info.toml", overwrite=True)
    for dirname in CURRICULUM_DIRS:
        _copy_path(src_root / dirname, path / dirname, overwrite=True)
    _sync_originals(path, src_root)
    _write_workspace_gitignore(path)
    return path


def update_workspace(path: Path) -> Path:
    path = path.expanduser().resolve()
    if not (path / "info.toml").exists():
        raise WorkspaceError(f"{path} is not a pylings workspace")

    src_root = source_root()
    _copy_path(src_root / "info.toml", path / "info.toml", overwrite=True)
    _copy_path(src_root / "checks", path / "checks", overwrite=True)
    _copy_path(src_root / "solutions", path / "solutions", overwrite=True)
    _copy_path(src_root / "exercises", path / "exercises", overwrite=False)
    _sync_originals(path, src_root)
    _write_workspace_gitignore(path)
    return path
