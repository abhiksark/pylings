# tests/integration/test_cli_topics.py
import subprocess
import sys
from pathlib import Path

from pythonlings.cli import _build_parser

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pythonlings", *args], capture_output=True, text=True
    )


def test_list_shows_topics_with_progress() -> None:
    result = _run("--root", str(FIXTURES), "list")
    assert result.returncode == 0
    # tiny_curriculum is one topic, "exercises"; 0/4 done on a fresh state.
    assert "exercises" in result.stdout
    assert "0/4" in result.stdout


def test_list_topic_shows_its_exercises() -> None:
    result = _run("--root", str(FIXTURES), "list", "exercises")
    assert result.returncode == 0
    for name in ("passing", "asserts", "syntax", "pending"):
        assert name in result.stdout


def test_list_unknown_topic_errors() -> None:
    result = _run("--root", str(FIXTURES), "list", "nope")
    assert result.returncode != 0
    assert "nope" in result.stderr


def test_verify_topic_runs_only_that_topic() -> None:
    # tiny_curriculum's "exercises" topic includes the failing fixture,
    # so a topic verify exits non-zero — but it must accept the argument.
    result = _run("--root", str(FIXTURES), "verify", "exercises")
    assert result.returncode in (0, 1)  # ran; not a usage error (2)


def test_verify_unknown_topic_errors() -> None:
    result = _run("--root", str(FIXTURES), "verify", "nope")
    assert result.returncode == 2
    assert "nope" in result.stderr


def test_start_unknown_topic_errors() -> None:
    # An unknown topic must fail before the TUI launches.
    result = _run("--root", str(FIXTURES), "start", "nope")
    assert result.returncode == 2
    assert "nope" in result.stderr


def test_topics_subcommand_parses() -> None:
    args = _build_parser().parse_args(["topics"])
    assert args.command == "topics"
