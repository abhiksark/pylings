# pylings/widgets/exercise_tree.py
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.widgets import Tree

if TYPE_CHECKING:
    from pylings.core.exercise import Exercise
    from pylings.core.manifest import Manifest
    from pylings.core.state import State


class ExerciseTree(Tree[str]):
    def __init__(self) -> None:
        super().__init__("exercises", id="tree")
        self.show_root = False

    def render_manifest(
        self, manifest: "Manifest", state: "State", current: str | None
    ) -> None:
        self.clear()
        topics: dict[str, object] = {}
        for ex in manifest.exercises:
            if ex.topic not in topics:
                topics[ex.topic] = self.root.add(ex.topic, expand=True)
            parent = topics[ex.topic]
            if ex.name in state.completed:
                marker = "✓"
            elif ex.name == current:
                marker = "●"
            else:
                marker = "🔒"
            parent.add_leaf(f"{marker} {ex.name}", data=ex.name)

    def render_topic(
        self,
        topic: str,
        exercises: list["Exercise"],
        completed: set[str],
        current: str | None,
    ) -> None:
        self.clear()
        node = self.root.add(topic, expand=True)
        for ex in exercises:
            if ex.name in completed:
                marker = "✓"
            elif ex.name == current:
                marker = "●"
            else:
                marker = "🔒"
            node.add_leaf(f"{marker} {ex.name}", data=ex.name)
