# Pylings Built-in Editor — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace external-editor launching with a built-in editor pane inside the pylings TUI, so a beginner edits the current exercise directly in pylings and the check re-runs automatically as they type.

**Architecture:** A new `EditorPane` widget wraps Textual's `TextArea`. The app composes editor + output side by side (exercise tree toggled on demand). Editing is debounced (600 ms) → the buffer is written to the exercise file → the check runs on a Textual thread worker → the result renders. The file watcher is removed entirely; action keys move to function keys so they don't collide with typing.

**Tech Stack:** Python ≥ 3.11 · Textual (`TextArea`, thread workers, timers) · `textual[syntax]` (tree-sitter Python grammar) · pytest · pytest-asyncio

**Spec:** `docs/superpowers/specs/2026-05-20-pylings-builtin-editor-design.md`

---

## File changes produced by this plan

```
pylings/
├── pyproject.toml                ← MODIFY  (drop watchfiles, textual → textual[syntax])
├── Readme.md                     ← MODIFY  (key table + workflow)
├── pylings/
│   ├── app.py                    ← REWRITE (in-pane editor, auto-save worker, F-keys)
│   ├── pylings.tcss              ← MODIFY  (editor|output layout, tree hidden)
│   ├── widgets/
│   │   ├── editor_pane.py        ← NEW     (EditorPane wraps TextArea)
│   │   └── output_panel.py       ← MODIFY  (reworded instruction + show_final)
│   └── core/
│       └── watcher.py            ← DELETE
└── tests/
    ├── unit/test_watcher.py      ← DELETE
    └── tui/
        ├── test_editor_pane.py   ← NEW
        └── test_app_pilot.py     ← REWRITE
```

Untouched: `pylings/core/{exercise,manifest,runner,state,reset}.py`, `pylings/cli.py`, `pylings/widgets/{progress,exercise_tree}.py`, all `tests/unit/` core tests, all `tests/integration/` tests.

---

## Task 1: Swap dependencies — drop watchfiles, add textual[syntax]

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Edit the `dependencies` array in `pyproject.toml`**

Replace this block:

```toml
dependencies = [
    "textual>=0.50.0",
    "watchfiles>=0.20.0",
]
```

with:

```toml
dependencies = [
    "textual[syntax]>=8.0.0",
]
```

Leave `[project.optional-dependencies]`, `[project.scripts]`, the hatch config, and `[tool.pytest.ini_options]` unchanged.

- [ ] **Step 2: Reinstall so the new extra is pulled in**

Run: `pip install -e ".[dev]"`
Expected: completes successfully; `textual[syntax]` pulls a `tree-sitter` Python grammar.

- [ ] **Step 3: Confirm nothing broke**

Run: `pytest -q`
Expected: `67 passed` (the `watchfiles` package is still physically installed in the environment, and `app.py` still imports it at this point — the dependency-list edit alone breaks nothing).

Note: if `python -c "import tree_sitter_python"` fails, syntax highlighting will degrade to monochrome — acceptable per the spec's graceful-fallback clause, but mention it in the report.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml
git commit -m "Swap watchfiles dependency for textual syntax extra

The file watcher is being removed in favour of a built-in editor, so
watchfiles is no longer needed. The textual[syntax] extra pulls the
tree-sitter Python grammar that powers editor syntax highlighting."
```

---

## Task 2: Add the EditorPane widget

**Files:**
- Create: `pylings/widgets/editor_pane.py`
- Test: `tests/tui/test_editor_pane.py`

- [ ] **Step 1: Write the failing test**

`tests/tui/test_editor_pane.py`:

```python
# tests/tui/test_editor_pane.py
from pathlib import Path

import pytest
from textual.app import App, ComposeResult
from textual.widgets import TextArea

from pylings.core.exercise import Exercise
from pylings.widgets.editor_pane import EditorPane


class _Harness(App[None]):
    def compose(self) -> ComposeResult:
        yield EditorPane()


@pytest.mark.asyncio
async def test_load_exercise_fills_editor(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("a = 1\nb = 2\n", encoding="utf-8")
    exercise = Exercise(name="ex", path=file, topic="t", hint="")

    app = _Harness()
    async with app.run_test() as pilot:
        await pilot.pause()
        pane = app.query_one(EditorPane)
        pane.load_exercise(exercise)
        await pilot.pause()
        assert pane.text == "a = 1\nb = 2\n"


@pytest.mark.asyncio
async def test_text_property_reflects_buffer(tmp_path: Path) -> None:
    app = _Harness()
    async with app.run_test() as pilot:
        await pilot.pause()
        pane = app.query_one(EditorPane)
        pane.query_one("#code", TextArea).text = "x = 42\n"
        await pilot.pause()
        assert pane.text == "x = 42\n"


@pytest.mark.asyncio
async def test_focus_editor_focuses_the_text_area(tmp_path: Path) -> None:
    app = _Harness()
    async with app.run_test() as pilot:
        await pilot.pause()
        pane = app.query_one(EditorPane)
        pane.focus_editor()
        await pilot.pause()
        assert app.focused is pane.query_one("#code", TextArea)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/tui/test_editor_pane.py -v`
Expected: `ModuleNotFoundError: No module named 'pylings.widgets.editor_pane'`

- [ ] **Step 3: Write `pylings/widgets/editor_pane.py`**

```python
# pylings/widgets/editor_pane.py
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import TextArea

from pylings.core.exercise import Exercise


class EditorPane(Vertical):
    """The in-TUI code editor for the current exercise."""

    def compose(self) -> ComposeResult:
        try:
            editor = TextArea.code_editor("", language="python", id="code")
        except Exception:
            # tree-sitter Python grammar unavailable — fall back to plain text.
            editor = TextArea.code_editor("", id="code")
        yield editor

    def load_exercise(self, exercise: Exercise) -> None:
        """Replace the editor contents with the exercise file from disk."""
        area = self.query_one("#code", TextArea)
        area.text = exercise.path.read_text(encoding="utf-8")
        area.move_cursor((0, 0))

    def focus_editor(self) -> None:
        self.query_one("#code", TextArea).focus()

    @property
    def text(self) -> str:
        return self.query_one("#code", TextArea).text
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/tui/test_editor_pane.py -v`
Expected: `3 passed`

- [ ] **Step 5: Run the full suite**

Run: `pytest -q`
Expected: `70 passed` (67 + 3 new).

- [ ] **Step 6: Commit**

```bash
git add pylings/widgets/editor_pane.py tests/tui/test_editor_pane.py
git commit -m "Add EditorPane widget wrapping Textual's TextArea

EditorPane is a thin Vertical container around a code-editor TextArea.
load_exercise() reads an exercise file into the buffer, the text
property reads it back, and focus_editor() puts the cursor in it.
Falls back to a plain (unhighlighted) editor if the Python grammar
isn't installed."
```

---

## Task 3: Rewrite the TUI for in-pane editing

**Files:**
- Rewrite: `pylings/app.py`
- Modify: `pylings/widgets/output_panel.py`
- Modify: `pylings/pylings.tcss`
- Delete: `pylings/core/watcher.py`, `tests/unit/test_watcher.py`
- Rewrite: `tests/tui/test_app_pilot.py`

This is the core task. The app rewrite, the watcher deletion, and the test rewrite are one atomic change — the package would not import with a half-applied version. Do the steps in order.

- [ ] **Step 1: Rewrite `tests/tui/test_app_pilot.py` with the new behavior**

This replaces the whole file. The tests fail against the current app — that is the TDD red phase.

```python
# tests/tui/test_app_pilot.py
import shutil
from pathlib import Path

import pytest
from textual.widgets import TextArea

from pylings.app import PylingsApp
from pylings.widgets.editor_pane import EditorPane
from pylings.widgets.exercise_tree import ExerciseTree

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _work_copy(tmp_path: Path) -> Path:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    return work


async def _settle(pilot) -> None:
    """Let mount-time runs — and any chained auto-advance — finish.

    The first fixture exercise (`passing`) passes immediately, so on mount
    the app runs it, advances, and runs the next one. Each run is a thread
    worker; waiting for workers repeatedly drains the whole chain.
    """
    for _ in range(6):
        await pilot.app.workers.wait_for_complete()
        await pilot.pause()


@pytest.mark.asyncio
async def test_app_launches_and_shows_progress(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        progress = str(app.query_one("#progress").render())
        assert "/4" in progress


@pytest.mark.asyncio
async def test_welcome_message_is_shown_as_subtitle(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert app.sub_title == app.manifest.welcome_message


@pytest.mark.asyncio
async def test_editor_loads_current_exercise(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        current = app.state.current
        assert current is not None
        expected = (work / "exercises" / f"{current}.py").read_text(encoding="utf-8")
        assert app.query_one("#code", TextArea).text == expected


@pytest.mark.asyncio
async def test_output_header_names_the_exercise(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        header = str(app.query_one("#output-header").render())
        assert ".py" in header


@pytest.mark.asyncio
async def test_f1_toggles_hint(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        hint = app.query_one("#hint")
        assert "visible" not in hint.classes
        await pilot.press("f1")
        await pilot.pause()
        assert "visible" in hint.classes


@pytest.mark.asyncio
async def test_f3_toggles_tree(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        tree = app.query_one(ExerciseTree)
        before = tree.display
        await pilot.press("f3")
        await pilot.pause()
        assert tree.display != before


@pytest.mark.asyncio
async def test_ctrl_q_quits(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        await pilot.press("ctrl+q")


@pytest.mark.asyncio
async def test_f2_resets_current_file(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        current = app.state.current
        assert current is not None
        target = work / "exercises" / f"{current}.py"
        original = target.read_text(encoding="utf-8")

        app.query_one("#code", TextArea).text = "# scrambled\n"
        app._flush_and_run()
        await _settle(pilot)
        assert target.read_text(encoding="utf-8") == "# scrambled\n"

        await pilot.press("f2")
        await _settle(pilot)
        assert app.query_one("#code", TextArea).text == original
        assert target.read_text(encoding="utf-8") == original


@pytest.mark.asyncio
async def test_typing_triggers_autosave(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        current = app.state.current
        assert current is not None
        target = work / "exercises" / f"{current}.py"

        app.query_one("#code", TextArea).text = "raise SystemExit(7)\n"
        # Wait past the 0.6s debounce so the timer fires on its own.
        await pilot.pause(1.0)
        await _settle(pilot)
        assert target.read_text(encoding="utf-8") == "raise SystemExit(7)\n"


@pytest.mark.asyncio
async def test_solving_advances_to_next_exercise(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        before = app.state.current
        assert before is not None

        # A solution with no `# I AM NOT DONE` marker that exits 0.
        app.query_one("#code", TextArea).text = "assert 1 + 1 == 2\n"
        app._flush_and_run()
        await _settle(pilot)

        assert before in app.state.completed
        assert app.state.current != before
        # The editor has loaded whatever exercise is now current.
        if app.state.current is not None:
            loaded = (work / "exercises" / f"{app.state.current}.py").read_text(
                encoding="utf-8"
            )
            assert app.query_one("#code", TextArea).text == loaded
```

- [ ] **Step 2: Run the new tests to verify they fail**

Run: `pytest tests/tui/test_app_pilot.py -q`
Expected: failures/errors (the current app has no `EditorPane`, no `#code`, uses letter bindings, has no `_flush_and_run`).

- [ ] **Step 3: Delete the watcher module and its test**

```bash
git rm pylings/core/watcher.py tests/unit/test_watcher.py
```

- [ ] **Step 4: Rewrite `pylings/widgets/output_panel.py`**

This rewords the instruction (editing is now in-pane, not external) and adds a `show_final` method for the curriculum-complete screen.

```python
# pylings/widgets/output_panel.py
from __future__ import annotations

import os

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from pylings.core.exercise import Exercise, RunResult

_INSTRUCTION = (
    "Edit the code on the left. "
    "The checks below update automatically as you type."
)


class OutputPanel(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("", id="output-header")
        yield Static("Loading…", id="output-body")
        yield Static("", id="hint")

    def render_result(self, exercise: Exercise, result: RunResult) -> None:
        self._render_header(exercise)
        body = self.query_one("#output-body", Static)
        self.remove_class("passed", "failed", "pending")
        if result.timed_out:
            self.add_class("failed")
            body.update(
                "[bold red]Not passing yet[/bold red]\n\n"
                f"Timed out after {result.duration_s:.1f}s — is there an infinite loop?"
            )
            return
        if result.exit_code != 0:
            self.add_class("failed")
            body.update(
                "[bold red]Not passing yet[/bold red]\n\n"
                f"{(result.stderr or result.stdout).rstrip()}"
            )
            return
        if exercise.is_pending():
            self.add_class("pending")
            body.update(
                "[bold yellow]Checks pass![/bold yellow]\n\n"
                "Remove the [yellow]# I AM NOT DONE[/yellow] line from the code "
                "on the left to advance to the next exercise."
            )
            return
        self.add_class("passed")
        body.update(
            f"[bold green]✓ {exercise.name} complete[/bold green]\n\n"
            f"{result.stdout}".rstrip()
        )

    def show_final(self, message: str) -> None:
        """Render the curriculum-complete screen."""
        self.remove_class("failed", "pending")
        self.add_class("passed")
        self.query_one("#output-header", Static).update(
            "[bold green]All exercises complete[/bold green]"
        )
        self.query_one("#output-body", Static).update(message)

    def _render_header(self, exercise: Exercise) -> None:
        header = self.query_one("#output-header", Static)
        header.update(
            f"[bold]{exercise.name}[/bold]   [dim]{self._display_path(exercise)}[/dim]\n"
            f"{_INSTRUCTION}"
        )

    @staticmethod
    def _display_path(exercise: Exercise) -> str:
        # Prefer a short path relative to the working directory; fall back to
        # the absolute path when that isn't possible (e.g. different drives).
        try:
            return os.path.relpath(exercise.path)
        except ValueError:
            return str(exercise.path)

    def toggle_hint(self, text: str) -> None:
        hint = self.query_one("#hint", Static)
        if "visible" in hint.classes:
            hint.remove_class("visible")
        else:
            hint.add_class("visible")
            hint.update(f"[italic]Hint:[/italic] {text or '(no hint provided)'}")
```

- [ ] **Step 5: Rewrite `pylings/pylings.tcss`**

```css
Screen {
    layout: vertical;
}

#progress {
    height: 1;
    background: $primary 30%;
    color: $text;
    padding: 0 1;
}

#main {
    layout: horizontal;
    height: 1fr;
}

#tree {
    width: 25%;
    border-right: solid $primary;
    padding: 1;
    display: none;
}

#editor {
    width: 1fr;
    border-right: solid $primary;
}

#editor #code {
    height: 1fr;
}

#output {
    width: 1fr;
    padding: 1;
}

#output-header {
    padding: 0 0 1 0;
    border-bottom: solid $primary;
    color: $text;
}

#output-body {
    padding: 1 0 0 0;
}

#output.passed {
    background: $success 20%;
}

#output.failed {
    background: $error 20%;
}

#output.pending {
    background: $warning 20%;
}

#hint {
    border-top: dashed $secondary;
    padding: 1 0;
    display: none;
}

#hint.visible {
    display: block;
}
```

- [ ] **Step 6: Rewrite `pylings/app.py`**

```python
# pylings/app.py
from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.timer import Timer
from textual.widgets import Footer, Header, TextArea

from pylings.core.exercise import Exercise, RunResult
from pylings.core.manifest import Manifest, load as load_manifest
from pylings.core.runner import run as run_exercise
from pylings.core.state import State, load as load_state, save as save_state
from pylings.widgets.editor_pane import EditorPane
from pylings.widgets.exercise_tree import ExerciseTree
from pylings.widgets.output_panel import OutputPanel
from pylings.widgets.progress import ProgressBar

_DEBOUNCE_SECONDS = 0.6


class PylingsApp(App[int]):
    CSS_PATH = "pylings.tcss"
    BINDINGS = [
        Binding("f1", "toggle_hint", "Hint"),
        Binding("f2", "reset", "Reset"),
        Binding("f3", "toggle_list", "List"),
        Binding("ctrl+q", "quit", "Quit"),
    ]

    def __init__(self, root: Path) -> None:
        super().__init__()
        self.root = root
        self.manifest: Manifest = load_manifest(root)
        self.state: State = load_state(root)
        if self.state.current is None:
            self.state.current = self.state.next_pending(self.manifest)
        self._save_timer: Timer | None = None
        # The editor content as last loaded from disk. Used to tell a real
        # edit apart from the Changed event that a programmatic load emits.
        self._loaded_text = ""

    def compose(self) -> ComposeResult:
        yield Header()
        yield ProgressBar(id="progress")
        yield Horizontal(
            ExerciseTree(),
            EditorPane(id="editor"),
            OutputPanel(id="output"),
            id="main",
        )
        yield Footer()

    def on_mount(self) -> None:
        self.title = "pylings"
        self.sub_title = self.manifest.welcome_message
        self._render_state()
        self._load_current()
        self._run_current()
        self.query_one(EditorPane).focus_editor()

    # --- rendering -------------------------------------------------------

    def _render_state(self) -> None:
        self.query_one(ExerciseTree).render_manifest(self.manifest, self.state)
        self.query_one(ProgressBar).update_progress(
            len(self.state.completed), len(self.manifest.exercises)
        )

    def _load_current(self) -> None:
        """Load the current exercise file into the editor (no run)."""
        if self.state.current is None:
            return
        exercise = self.manifest.by_name(self.state.current)
        pane = self.query_one(EditorPane)
        pane.load_exercise(exercise)
        self._loaded_text = pane.text

    # --- the auto-save / run loop ---------------------------------------

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        # Ignore the Changed event emitted by a programmatic load, and any
        # edit that lands the buffer back on the loaded baseline.
        if self.query_one(EditorPane).text == self._loaded_text:
            return
        if self._save_timer is not None:
            self._save_timer.stop()
        self._save_timer = self.set_timer(_DEBOUNCE_SECONDS, self._flush_and_run)

    def _flush_and_run(self) -> None:
        self._save_timer = None
        if self.state.current is None:
            return
        exercise = self.manifest.by_name(self.state.current)
        exercise.path.write_text(self.query_one(EditorPane).text, encoding="utf-8")
        self._run_current()

    def _run_current(self) -> None:
        if self.state.current is None:
            return
        exercise = self.manifest.by_name(self.state.current)
        self.run_worker(
            lambda: self._run_blocking(exercise), exclusive=True, thread=True
        )

    def _run_blocking(self, exercise: Exercise) -> None:
        # Runs on a worker thread; never touches widgets directly.
        result = run_exercise(exercise)
        self.call_from_thread(self._apply_result, exercise, result)

    def _apply_result(self, exercise: Exercise, result: RunResult) -> None:
        self.query_one(OutputPanel).render_result(exercise, result)
        if not result.passed:
            return
        self.state.mark_done(exercise.name, self.manifest)
        save_state(self.root, self.state)
        self._render_state()
        if self.state.current is None:
            self.query_one(OutputPanel).show_final(self.manifest.final_message)
            return
        self._load_current()
        self._run_current()

    # --- actions ---------------------------------------------------------

    def action_toggle_hint(self) -> None:
        if self.state.current is None:
            return
        exercise = self.manifest.by_name(self.state.current)
        self.query_one(OutputPanel).toggle_hint(exercise.hint)

    def action_reset(self) -> None:
        from pylings.core.reset import restore

        if self.state.current is None:
            return
        if self._save_timer is not None:
            self._save_timer.stop()
            self._save_timer = None
        exercise = self.manifest.by_name(self.state.current)
        restore(self.root, exercise)
        self._load_current()
        self._run_current()

    def action_toggle_list(self) -> None:
        tree = self.query_one(ExerciseTree)
        tree.display = not tree.display

    def action_quit(self) -> None:
        # Flush a pending edit so the last keystrokes aren't lost on quit.
        if self._save_timer is not None:
            self._save_timer.stop()
            self._save_timer = None
            if self.state.current is not None:
                exercise = self.manifest.by_name(self.state.current)
                exercise.path.write_text(
                    self.query_one(EditorPane).text, encoding="utf-8"
                )
        self.exit(0)


def run_tui(root: Path) -> int:
    return PylingsApp(root).run() or 0
```

- [ ] **Step 7: Run the rewritten Pilot suite**

Run: `pytest tests/tui/test_app_pilot.py -q`
Expected: all tests pass (10 tests).

If a test hangs or fails on worker timing, the `_settle` helper may need more iterations — but do not weaken an assertion to make it pass. If genuinely stuck, report BLOCKED with the failing test and symptom.

- [ ] **Step 8: Run the full suite**

Run: `pytest -q`
Expected: green. Count ≈ 71 — 67 baseline, minus 2 (`test_watcher.py`) minus the old `test_app_pilot.py` count, plus 3 (`test_editor_pane.py`, Task 2) plus 10 (new `test_app_pilot.py`). The exact number isn't important; what matters is **0 failures**.

- [ ] **Step 9: Manual smoke test**

```bash
cd /home/abhik/Projects/personal/pylings
pylings --root .
```
Expected: the TUI opens with a code editor on the left showing `variables1`'s broken source, the check output on the right, and `F1 Hint · F2 Reset · F3 List · Ctrl+Q Quit` in the footer. Type into the editor — after you pause, the check re-runs. Press `Ctrl+Q` to exit. This is a visual check the headless tests cannot make; if the layout is broken, fix the CSS or compose order before committing.

- [ ] **Step 10: Commit**

```bash
git add pylings/app.py pylings/widgets/output_panel.py pylings/pylings.tcss tests/tui/test_app_pilot.py
git add -u
git commit -m "Replace external editing with a built-in editor pane

The TUI now hosts a code editor: the learner edits the current
exercise directly in pylings, and a debounced auto-save writes the
file and re-runs the check on a worker thread. Layout is editor and
output side by side, with the exercise tree toggled by F3. Action
keys move to F1/F2/F3/Ctrl+Q so they don't collide with typing. The
file watcher is deleted — nothing external drives runs anymore."
```

---

## Task 4: Update the README and run final verification

**Files:**
- Modify: `Readme.md`

- [ ] **Step 1: Update the TUI key table and workflow in `Readme.md`**

Find the `In the TUI:` section and its key table (currently listing `e`/`h`/`r`/`n`/`l`/`q`) plus the line that begins `Type \`pylings\` with no arguments`. Replace from `In the TUI:` down to the end of that paragraph with:

```markdown
In the TUI, you edit the exercise right inside pylings — a code editor
pane on the left, the live check result on the right. The check re-runs
automatically a moment after you stop typing; there is no save key.

| Key | Action |
|---|---|
| `F1` | Toggle hint |
| `F2` | Reset the current exercise |
| `F3` | Toggle the exercise list |
| `Ctrl+Q` | Quit |

Type `pylings` with no arguments and it resumes on whatever exercise you
haven't finished yet — the editor opens straight on it.
```

- [ ] **Step 2: Update the "How an exercise works" section**

Find the `## How an exercise works` section. Replace its body with:

```markdown
Each file in `exercises/` contains:
1. A `# I AM NOT DONE` line near the top (the gate).
2. Broken code you have to fix.
3. A block of `assert` statements at the bottom (the checks — don't edit).

Edit the code in the pylings editor pane. When the script exits 0 *and*
you've removed the `# I AM NOT DONE` line, pylings advances you to the
next exercise.
```

- [ ] **Step 3: Run the full suite one last time**

Run: `pytest -q`
Expected: 0 failures.

- [ ] **Step 4: Confirm the CLI subcommands still cold-start without Textual**

Run: `python -X importtime -m pylings --root tests/fixtures/tiny_curriculum list 2>&1 | grep -c "import 'textual'"`
Expected: `0` (the CLI subcommands must not import Textual — only the TUI path does).

- [ ] **Step 5: Commit**

```bash
git add Readme.md
git commit -m "Update README for the built-in editor workflow

Documents the in-pane editor, the F1/F2/F3/Ctrl+Q keys, and the
no-save-key auto-run loop."
```

---

## Done

After Task 4:

- `pylings` opens a TUI with a built-in code editor; the learner never needs an external editor or `$EDITOR`.
- Typing pauses trigger a debounced auto-save and a worker-thread check run.
- Solving an exercise (correct code, marker removed) advances to the next, which loads into the editor.
- `F1`/`F2`/`F3`/`Ctrl+Q` work without colliding with typing.
- The file watcher and the `watchfiles` dependency are gone; `textual[syntax]` is in.
- All spec success criteria are met:
  1. Editable pane on launch, no external editor — Task 2 + 3.
  2. Pause → auto-save + re-run — Task 3 (`on_text_area_changed` → `_flush_and_run` → worker).
  3. Correct solution + marker removed advances and loads next — Task 3 (`_apply_result`).
  4. `F1`/`F2`/`F3`/`Ctrl+Q` work while editing — Task 3 (function-key bindings).
  5. Syntax highlighting — Task 1 (`textual[syntax]`) + Task 2 (`language="python"`).
  6. `watchfiles` dropped, `textual[syntax]` added — Task 1.
  7. Full suite green — verified in Tasks 2, 3, 4.
