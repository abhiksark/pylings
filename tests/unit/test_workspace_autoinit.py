from __future__ import annotations

from pathlib import Path

from pylings.core.curriculum import ensure_workspace, init_workspace


def test_autoinits_workspace_in_empty_dir(tmp_path: Path) -> None:
    work, created = ensure_workspace(tmp_path)

    assert created is True
    assert work == (tmp_path / "pylings-workspace").resolve()
    assert (work / "info.toml").exists()


def test_returns_root_unchanged_when_already_a_workspace(tmp_path: Path) -> None:
    init_workspace(tmp_path)

    work, created = ensure_workspace(tmp_path)

    assert created is False
    assert work == tmp_path.resolve()


def test_reuses_previously_autoinited_workspace(tmp_path: Path) -> None:
    first, first_created = ensure_workspace(tmp_path)
    second, second_created = ensure_workspace(tmp_path)

    assert first_created is True
    assert second_created is False
    assert second == first
