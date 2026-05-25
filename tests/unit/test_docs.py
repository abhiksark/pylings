from pathlib import Path

from pylings.core.docs import load_snippet, load_topic_snippet
from pylings.core.manifest import load
from pylings.screens.docs import DocsScreen


def test_load_topic_snippet_returns_bundled_reference() -> None:
    snippet = load_topic_snippet("variables")
    assert snippet is not None
    assert snippet.topic == "variables"
    assert snippet.title == "Variables"
    assert snippet.source_url.startswith("https://docs.python.org/3/")
    assert "Assigning names" in snippet.text


def test_load_topic_snippet_returns_none_for_unknown_topic() -> None:
    assert load_topic_snippet("missing") is None


def test_load_snippet_falls_back_to_official_docs_url() -> None:
    snippet = load_snippet(
        "custom_topic",
        "https://docs.python.org/3/tutorial/introduction.html",
    )
    assert snippet is not None
    assert snippet.topic == "variables"
    assert "Assigning names" in snippet.text


def test_real_curriculum_topics_have_bundled_references() -> None:
    repo = Path(__file__).parents[2]
    manifest = load(repo)
    missing = [
        topic for topic in manifest.topics() if load_topic_snippet(topic) is None
    ]
    assert missing == []


def test_docs_screen_markdown_includes_configured_docs_for_all_exercises() -> None:
    repo = Path(__file__).parents[2]
    manifest = load(repo)

    missing = [
        ex.name
        for ex in manifest.exercises
        if ex.docs not in DocsScreen(ex)._reference_markdown()
    ]

    assert missing == []
