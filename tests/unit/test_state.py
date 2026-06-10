# tests/unit/test_state.py
from pathlib import Path

from pythonlings.core.state import State, load, save


def test_load_creates_fresh_state_when_missing(tmp_path: Path) -> None:
    state = load(tmp_path)
    assert state.completed == set()


def test_save_then_load_roundtrip(tmp_path: Path) -> None:
    save(tmp_path, State(completed={"a", "b"}))
    loaded = load(tmp_path)
    assert loaded.completed == {"a", "b"}


def test_save_then_load_ux_fields(tmp_path: Path) -> None:
    save(
        tmp_path,
        State(
            completed={"a"},
            seen_intro=True,
            last_topic="alpha",
            last_exercise="a2",
        ),
    )
    loaded = load(tmp_path)
    assert loaded.completed == {"a"}
    assert loaded.seen_intro is True
    assert loaded.last_topic == "alpha"
    assert loaded.last_exercise == "a2"


def test_missing_ux_fields_default_for_existing_v2_state(tmp_path: Path) -> None:
    import json

    pdir = tmp_path / ".pythonlings"
    pdir.mkdir()
    (pdir / "state.json").write_text(
        json.dumps({"format_version": 2, "completed": ["x"]}),
        encoding="utf-8",
    )
    loaded = load(tmp_path)
    assert loaded.completed == {"x"}
    assert loaded.seen_intro is False
    assert loaded.last_topic is None
    assert loaded.last_exercise is None


def test_state_file_is_format_version_2(tmp_path: Path) -> None:
    import json
    save(tmp_path, State(completed={"a"}))
    data = json.loads((tmp_path / ".pythonlings" / "state.json").read_text())
    assert data["format_version"] == 2
    assert data["completed"] == ["a"]


def test_old_v1_state_is_discarded(tmp_path: Path) -> None:
    import json
    pdir = tmp_path / ".pythonlings"
    pdir.mkdir()
    (pdir / "state.json").write_text(
        json.dumps({"format_version": 1, "completed": ["x"], "current": "y"}),
        encoding="utf-8",
    )
    state = load(tmp_path)
    assert state.completed == set()  # v1 discarded, fresh start
    assert (pdir / "state.json.bak").exists()


def test_corrupt_state_is_recovered(tmp_path: Path) -> None:
    pdir = tmp_path / ".pythonlings"
    pdir.mkdir()
    (pdir / "state.json").write_text("not json {{", encoding="utf-8")
    state = load(tmp_path)
    assert state.completed == set()
    assert (pdir / "state.json.bak").exists()


def test_mark_done_adds_to_completed(tmp_path: Path) -> None:
    state = State()
    state.mark_done("loops1")
    assert "loops1" in state.completed


def test_record_resume_marks_intro_seen() -> None:
    state = State()
    state.record_resume("alpha", "a1")
    assert state.seen_intro is True
    assert state.last_topic == "alpha"
    assert state.last_exercise == "a1"


def test_clear_resume_keeps_intro_seen() -> None:
    state = State(seen_intro=True, last_topic="alpha", last_exercise="a1")
    state.clear_resume()
    assert state.seen_intro is True
    assert state.last_topic is None
    assert state.last_exercise is None


def test_atomic_write_keeps_last_value(tmp_path: Path) -> None:
    save(tmp_path, State(completed={"x"}))
    save(tmp_path, State(completed={"y"}))
    assert load(tmp_path).completed == {"y"}
