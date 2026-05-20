# tests/unit/test_manifest.py
from pathlib import Path

import pytest

from pylings.core.manifest import Manifest, ManifestError, load

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _write_curriculum(
    root: Path, name: str, exercise_src: str = "", check_src: str = ""
) -> None:
    """Write a minimal one-exercise curriculum under `root`."""
    (root / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        f'name = "{name}"\n'
        f'path = "exercises/{name}.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    (root / "exercises").mkdir(exist_ok=True)
    (root / "exercises" / f"{name}.py").write_text(exercise_src, encoding="utf-8")
    (root / "checks").mkdir(exist_ok=True)
    (root / "checks" / f"{name}.py").write_text(check_src, encoding="utf-8")


def test_load_tiny_curriculum() -> None:
    manifest = load(FIXTURES)
    assert isinstance(manifest, Manifest)
    assert [ex.name for ex in manifest.exercises] == [
        "passing",
        "asserts",
        "syntax",
        "pending",
    ]
    assert manifest.welcome_message == "Welcome to the test curriculum."
    assert manifest.final_message == "All test exercises complete."
    assert manifest.exercises[0].topic == "exercises"
    assert manifest.exercises[0].hint.startswith("This one should always pass")


def test_check_path_is_derived() -> None:
    manifest = load(FIXTURES)
    check = manifest.by_name("passing").check_path
    assert check == FIXTURES / "checks" / "passing.py"


def test_load_defaults_messages_when_omitted(tmp_path: Path) -> None:
    _write_curriculum(tmp_path, "a")
    manifest = load(tmp_path)
    assert manifest.welcome_message == "Welcome to pylings!"
    assert manifest.final_message == "All exercises complete."


def test_load_rejects_missing_info_toml(tmp_path: Path) -> None:
    with pytest.raises(ManifestError, match="info.toml"):
        load(tmp_path)


def test_load_rejects_wrong_format_version(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text("format_version = 2\n", encoding="utf-8")
    with pytest.raises(ManifestError, match="format_version"):
        load(tmp_path)


def test_load_rejects_empty_exercises_list(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text("format_version = 1\n", encoding="utf-8")
    with pytest.raises(ManifestError, match="non-empty"):
        load(tmp_path)


def test_load_rejects_missing_exercise_path(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'path = "exercises/missing.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    with pytest.raises(ManifestError, match="exercises/missing.py"):
        load(tmp_path)


def test_load_rejects_path_not_under_exercises(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'path = "lessons/a.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    with pytest.raises(ManifestError, match="under exercises/"):
        load(tmp_path)


def test_load_rejects_missing_check_file(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        "[[exercises]]\n"
        'name = "a"\n'
        'path = "exercises/a.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "a.py").write_text("", encoding="utf-8")
    # No checks/a.py created.
    with pytest.raises(ManifestError, match="check file"):
        load(tmp_path)


def test_load_rejects_duplicate_names(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        "format_version = 1\n"
        '[[exercises]]\nname = "a"\npath = "exercises/a.py"\nhint = "h"\n'
        '[[exercises]]\nname = "a"\npath = "exercises/b.py"\nhint = "h"\n',
        encoding="utf-8",
    )
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "a.py").write_text("", encoding="utf-8")
    (tmp_path / "exercises" / "b.py").write_text("", encoding="utf-8")
    (tmp_path / "checks").mkdir()
    (tmp_path / "checks" / "a.py").write_text("", encoding="utf-8")
    (tmp_path / "checks" / "b.py").write_text("", encoding="utf-8")
    with pytest.raises(ManifestError, match="duplicate"):
        load(tmp_path)


def test_manifest_by_name_and_index_of() -> None:
    manifest = load(FIXTURES)
    assert manifest.by_name("asserts").name == "asserts"
    assert manifest.index_of("syntax") == 2
    with pytest.raises(KeyError):
        manifest.by_name("nope")


def test_topics_in_first_appearance_order() -> None:
    manifest = load(FIXTURES)
    # tiny_curriculum's exercises all live directly under exercises/,
    # so they share the single topic "exercises".
    assert manifest.topics() == ["exercises"]


def test_exercises_in_returns_topic_members_in_order() -> None:
    manifest = load(FIXTURES)
    names = [ex.name for ex in manifest.exercises_in("exercises")]
    assert names == ["passing", "asserts", "syntax", "pending"]


def test_exercises_in_unknown_topic_is_empty() -> None:
    manifest = load(FIXTURES)
    assert manifest.exercises_in("nope") == []
