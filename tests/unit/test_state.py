# tests/unit/test_state.py

from pathlib import Path

import pytest

from pylings.core.exercise import Exercise
from pylings.core.manifest import Manifest
from pylings.core.state import State, load, save

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _manifest_from_fixtures() -> Manifest:
    from pylings.core.manifest import load as load_manifest
    return load_manifest(FIXTURES)


def test_load_creates_fresh_state_when_missing(tmp_path: Path) -> None:
    state = load(tmp_path)
    assert state.completed == set()
    assert state.current is None


def test_save_then_load_roundtrip(tmp_path: Path) -> None:
    state = State(completed={"a", "b"}, current="c")
    save(tmp_path, state)
    loaded = load(tmp_path)
    assert loaded.completed == {"a", "b"}
    assert loaded.current == "c"


def test_state_file_is_json_with_sorted_array(tmp_path: Path) -> None:
    save(tmp_path, State(completed={"b", "a", "c"}, current=None))
    raw = (tmp_path / ".pylings" / "state.json").read_text()
    assert '"completed": [\n    "a",\n    "b",\n    "c"\n  ]' in raw or '"completed": ["a", "b", "c"]' in raw


def test_corrupt_state_is_recovered(tmp_path: Path) -> None:
    pylings_dir = tmp_path / ".pylings"
    pylings_dir.mkdir()
    (pylings_dir / "state.json").write_text("not json {{", encoding="utf-8")

    state = load(tmp_path)
    assert state.completed == set()
    assert state.current is None
    assert (pylings_dir / "state.json.bak").exists()


def test_mark_done_updates_current(tmp_path: Path) -> None:
    manifest = _manifest_from_fixtures()
    state = State(completed=set(), current="passing")
    state.mark_done("passing", manifest)
    assert "passing" in state.completed
    assert state.current == "asserts"


def test_mark_done_last_exercise_sets_current_none(tmp_path: Path) -> None:
    manifest = _manifest_from_fixtures()
    state = State(
        completed={"passing", "asserts", "syntax"},
        current="pending",
    )
    state.mark_done("pending", manifest)
    assert state.current is None


def test_next_pending_walks_to_first_uncompleted() -> None:
    manifest = _manifest_from_fixtures()
    state = State(completed={"passing"}, current=None)
    assert state.next_pending(manifest) == "asserts"


def test_atomic_write_does_not_leave_partial_file(tmp_path: Path) -> None:
    save(tmp_path, State(completed={"x"}, current=None))
    save(tmp_path, State(completed={"y"}, current=None))
    loaded = load(tmp_path)
    assert loaded.completed == {"y"}
