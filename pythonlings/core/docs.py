# pythonlings/core/docs.py
from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from typing import Any
from urllib.parse import urldefrag


@dataclass(frozen=True)
class DocSnippet:
    topic: str
    title: str
    source_url: str
    text: str


def load_topic_snippet(topic: str) -> DocSnippet | None:
    """Load the bundled local docs snippet for a curriculum topic."""
    index = _load_index()
    if index is None:
        return None

    entry = index["topics"].get(topic)
    if entry is None:
        return None

    return _load_entry(topic, entry)


def load_snippet(topic: str, source_url: str = "") -> DocSnippet | None:
    """Load a bundled snippet by topic, falling back to an official docs URL."""
    index = _load_index()
    if index is None:
        return None

    entry = index["topics"].get(topic)
    if entry is not None:
        return _load_entry(topic, entry)

    normalized_source = _normalize_url(source_url)
    if not normalized_source:
        return None

    for candidate_topic, candidate_entry in index["topics"].items():
        candidate_source = candidate_entry["source_url"]
        if (
            candidate_source == source_url
            or _normalize_url(candidate_source) == normalized_source
        ):
            return _load_entry(candidate_topic, candidate_entry)

    return None


def _load_index() -> dict[str, Any] | None:
    try:
        docs_root = resources.files("pythonlings.docs")
        return json.loads((docs_root / "index.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, ModuleNotFoundError):
        return None


def _load_entry(topic: str, entry: dict[str, Any]) -> DocSnippet | None:
    try:
        docs_root = resources.files("pythonlings.docs")
        text = (docs_root / entry["file"]).read_text(encoding="utf-8").strip()
    except (FileNotFoundError, KeyError, ModuleNotFoundError):
        return None

    return DocSnippet(
        topic=topic,
        title=entry["title"],
        source_url=entry["source_url"],
        text=text,
    )


def _normalize_url(url: str) -> str:
    return urldefrag(url.strip()).url
