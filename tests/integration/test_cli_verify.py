# tests/integration/test_cli_verify.py
import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pylings", *args],
        capture_output=True,
        text=True,
    )


def test_verify_fails_on_first_failure() -> None:
    # passing.py passes, asserts.py fails → verify exits non-zero.
    result = _run("--root", str(FIXTURES), "verify")
    assert result.returncode != 0
    assert "asserts" in (result.stdout + result.stderr)


def test_verify_against_only_passing_fixture(tmp_path: Path) -> None:
    info = tmp_path / "info.toml"
    info.write_text(
        'format_version = 1\n'
        '[[exercises]]\n'
        'name = "ok"\n'
        'path = "exercises/ok.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "ok.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "checks").mkdir()
    (tmp_path / "checks" / "ok.py").write_text("assert x == 1\n", encoding="utf-8")

    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 0, result.stderr


def test_verify_ignores_marker(tmp_path: Path) -> None:
    # An exercise with the marker still in place and checks passing
    # should be treated as a verify-pass.
    info = tmp_path / "info.toml"
    info.write_text(
        'format_version = 1\n'
        '[[exercises]]\nname = "ok"\npath = "exercises/ok.py"\nhint = "h"\n',
        encoding="utf-8",
    )
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "ok.py").write_text(
        "# I AM NOT DONE\nx = 1\n", encoding="utf-8"
    )
    (tmp_path / "checks").mkdir()
    (tmp_path / "checks" / "ok.py").write_text("assert x == 1\n", encoding="utf-8")

    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 0


def test_verify_reports_manifest_error_with_exit_2(tmp_path: Path) -> None:
    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 2
    assert "info.toml" in result.stderr
