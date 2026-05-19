# tests/integration/test_cli_cold_start.py
import subprocess
import sys
import time
from pathlib import Path

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _cold_start_ms(*args: str) -> str:
    # Run the subprocess with `-X importtime` and grep for textual.
    # We don't measure wall-clock for the test (CI flake); we assert that
    # textual was never imported in the subcommand path.
    proc = subprocess.run(
        [sys.executable, "-X", "importtime", "-m", "pylings", "--root", str(FIXTURES), *args],
        capture_output=True,
        text=True,
    )
    return proc.stderr  # importtime output goes to stderr


def test_hint_does_not_import_textual() -> None:
    out = _cold_start_ms("hint", "passing")
    assert "import 'textual'" not in out, f"textual loaded for `pylings hint`:\n{out}"


def test_list_does_not_import_textual() -> None:
    out = _cold_start_ms("list")
    assert "import 'textual'" not in out


def test_verify_does_not_import_textual() -> None:
    out = _cold_start_ms("verify")
    assert "import 'textual'" not in out


def test_run_does_not_import_textual() -> None:
    out = _cold_start_ms("run", "passing")
    assert "import 'textual'" not in out
