from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pylings", *args],
        capture_output=True,
        text=True,
    )


def test_launch_in_empty_dir_autoinits_workspace(tmp_path: Path) -> None:
    # `start` with a non-existent topic returns before launching the TUI, so we
    # can assert the auto-init side effect without needing a terminal.
    _run("--root", str(tmp_path), "start", "__no_such_topic__")

    assert (tmp_path / "pylings-workspace" / "info.toml").exists()
