# tests/unit/test_manifest.py
from pathlib import Path

import pytest

from pylings.core.manifest import Manifest, ManifestError, load

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def test_load_tiny_curriculum() -> None:
    manifest = load(FIXTURES)
    assert isinstance(manifest, Manifest)
    assert [ex.name for ex in manifest.exercises] == ["passing", "asserts", "syntax", "pending"]
    assert manifest.welcome_message == "Welcome to the test curriculum."
    assert manifest.final_message == "All test exercises complete."
    assert manifest.exercises[0].topic == "exercises"  # parent dir of the path
    assert manifest.exercises[0].hint.startswith("This one should always pass")


def test_load_defaults_messages_when_omitted(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        'format_version = 1\n'
        '[[exercises]]\n'
        'name = "a"\n'
        'path = "exercises/a.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "a.py").write_text("", encoding="utf-8")

    manifest = load(tmp_path)
    assert manifest.welcome_message == "Welcome to pylings!"
    assert manifest.final_message == "All exercises complete."


def test_load_rejects_missing_info_toml(tmp_path: Path) -> None:
    with pytest.raises(ManifestError, match="info.toml"):
        load(tmp_path)


def test_load_rejects_wrong_format_version(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text('format_version = 2\n', encoding="utf-8")
    with pytest.raises(ManifestError, match="format_version"):
        load(tmp_path)


def test_load_rejects_empty_exercises_list(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text('format_version = 1\n', encoding="utf-8")
    with pytest.raises(ManifestError, match="non-empty"):
        load(tmp_path)


def test_load_rejects_missing_exercise_path(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        'format_version = 1\n'
        '[[exercises]]\n'
        'name = "a"\n'
        'path = "exercises/missing.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    with pytest.raises(ManifestError, match="exercises/missing.py"):
        load(tmp_path)


def test_load_rejects_duplicate_names(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        'format_version = 1\n'
        '[[exercises]]\nname = "a"\npath = "exercises/a.py"\nhint = "h"\n'
        '[[exercises]]\nname = "a"\npath = "exercises/b.py"\nhint = "h"\n',
        encoding="utf-8",
    )
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "a.py").write_text("", encoding="utf-8")
    (tmp_path / "exercises" / "b.py").write_text("", encoding="utf-8")
    with pytest.raises(ManifestError, match="duplicate"):
        load(tmp_path)


def test_manifest_by_name_and_index_of() -> None:
    manifest = load(FIXTURES)
    assert manifest.by_name("asserts").name == "asserts"
    assert manifest.index_of("syntax") == 2
    with pytest.raises(KeyError):
        manifest.by_name("nope")
