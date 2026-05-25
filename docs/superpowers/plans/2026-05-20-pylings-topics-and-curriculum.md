# Pylings Topic Tracks & Curriculum Expansion — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn pylings into per-topic tracks (a topic picker, each topic an independent linear sequence) and grow the curriculum to 31 topics / ~300 exercises.

**Architecture:** Topics are derived from exercise directory names — no `info.toml` format change. The state model simplifies to a flat `completed` set (`format_version` 2); per-topic progress is derived. The TUI becomes two Textual screens — a topic picker and a per-topic track. The curriculum is authored one topic per task following a fixed exercise template.

**Tech Stack:** Python ≥ 3.11 · Textual (multi-screen) · `tomllib` · pytest

**Spec:** `docs/superpowers/specs/2026-05-20-pylings-topics-and-curriculum-design.md`

---

## The two phases

- **Phase 1 — the feature (Tasks 1–5):** state v2, manifest topic helpers, CLI topic commands, a multi-topic test fixture, the two-screen TUI. After Phase 1, pylings is a working topic-navigation tool over the existing 3 exercises.
- **Phase 2 — the content (Tasks 6–36):** 31 topic-authoring tasks, one per topic, each following the shared **Topic Authoring Procedure** below. Each adds one complete topic and is independently shippable.

Phase 1 tasks are ordered so the suite stays green after each. Phase 2 tasks are independent of each other.

---

## File structure

```
pylings/core/
  state.py         MODIFY — flat completed set, format_version 2
  manifest.py      MODIFY — topics() / exercises_in() helpers
pylings/
  cli.py           MODIFY — topic-aware list / start / verify
  app.py           REWRITE — App shell hosting two screens
  screens/         NEW package
    __init__.py
    topic_picker.py  NEW — TopicPickerScreen
    track.py         NEW — TrackScreen (the editor/auto-save loop)
  pylings.tcss     MODIFY — styles for the picker
tests/
  fixtures/multi_topic/   NEW — small 2-topic fixture
  unit/test_state.py      MODIFY
  unit/test_manifest.py   MODIFY
  integration/test_cli_*  MODIFY
  tui/test_app_pilot.py   REWRITE — picker + track Pilot tests
exercises/<topic>/         NEW dirs (Phase 2)
checks/<topic>/            NEW dirs (Phase 2)
info.toml                  MODIFY (Phase 2 — one block of entries per topic)
```

---

# Phase 1 — The feature

## Task 1: Manifest topic helpers

Purely additive — two methods on `Manifest`. Nothing else changes, so the suite stays green.

**Files:**
- Modify: `pylings/core/manifest.py`
- Test: `tests/unit/test_manifest.py`

- [ ] **Step 1: Write the failing test** — append to `tests/unit/test_manifest.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_manifest.py -k topic -v`
Expected: `AttributeError: 'Manifest' object has no attribute 'topics'`

- [ ] **Step 3: Add the two methods** to the `Manifest` dataclass in `pylings/core/manifest.py`, after `index_of`:

```python
    def topics(self) -> list[str]:
        """Topic names in first-appearance order."""
        ordered: list[str] = []
        for ex in self.exercises:
            if ex.topic not in ordered:
                ordered.append(ex.topic)
        return ordered

    def exercises_in(self, topic: str) -> list[Exercise]:
        """Exercises belonging to one topic, in curriculum order."""
        return [ex for ex in self.exercises if ex.topic == topic]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/test_manifest.py -k topic -v`
Expected: 3 passed.

- [ ] **Step 5: Run the full suite**

Run: `pytest -q`
Expected: 0 failures.

- [ ] **Step 6: Commit**

```bash
git add pylings/core/manifest.py tests/unit/test_manifest.py
git commit -m "Add Manifest.topics() and exercises_in() helpers

Topics are derived from exercise directory names; topics() returns
them in first-appearance order and exercises_in() returns one topic's
exercises in curriculum order. Purely additive."
```

---

## Task 2: State v2 — flat completed set

Rewrite `state.py` to drop the global `current` cursor. This ripples to `cli.py` and `app.py`, which currently read `state.current` / call `state.next_pending` — they are updated in the same task to compute "first uncompleted exercise" from the flat set, keeping the existing single-screen behavior working (the two-screen TUI comes in Task 5).

**Files:**
- Rewrite: `pylings/core/state.py`
- Modify: `pylings/cli.py`, `pylings/app.py`
- Rewrite: `tests/unit/test_state.py`

- [ ] **Step 1: Rewrite `tests/unit/test_state.py`** (full file):

```python
# tests/unit/test_state.py
from pathlib import Path

from pylings.core.state import State, load, save


def test_load_creates_fresh_state_when_missing(tmp_path: Path) -> None:
    state = load(tmp_path)
    assert state.completed == set()


def test_save_then_load_roundtrip(tmp_path: Path) -> None:
    save(tmp_path, State(completed={"a", "b"}))
    loaded = load(tmp_path)
    assert loaded.completed == {"a", "b"}


def test_state_file_is_format_version_2(tmp_path: Path) -> None:
    import json
    save(tmp_path, State(completed={"a"}))
    data = json.loads((tmp_path / ".pylings" / "state.json").read_text())
    assert data["format_version"] == 2
    assert data["completed"] == ["a"]


def test_old_v1_state_is_discarded(tmp_path: Path) -> None:
    import json
    pdir = tmp_path / ".pylings"
    pdir.mkdir()
    (pdir / "state.json").write_text(
        json.dumps({"format_version": 1, "completed": ["x"], "current": "y"}),
        encoding="utf-8",
    )
    state = load(tmp_path)
    assert state.completed == set()  # v1 discarded, fresh start
    assert (pdir / "state.json.bak").exists()


def test_corrupt_state_is_recovered(tmp_path: Path) -> None:
    pdir = tmp_path / ".pylings"
    pdir.mkdir()
    (pdir / "state.json").write_text("not json {{", encoding="utf-8")
    state = load(tmp_path)
    assert state.completed == set()
    assert (pdir / "state.json.bak").exists()


def test_mark_done_adds_to_completed(tmp_path: Path) -> None:
    state = State()
    state.mark_done("loops1")
    assert "loops1" in state.completed


def test_atomic_write_keeps_last_value(tmp_path: Path) -> None:
    save(tmp_path, State(completed={"x"}))
    save(tmp_path, State(completed={"y"}))
    assert load(tmp_path).completed == {"y"}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_state.py -q`
Expected: failures (`State` still requires/has `current`).

- [ ] **Step 3: Rewrite `pylings/core/state.py`** (full file):

```python
# pylings/core/state.py

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

FORMAT_VERSION = 2


@dataclass
class State:
    completed: set[str] = field(default_factory=set)

    def mark_done(self, name: str) -> None:
        self.completed.add(name)


def _state_path(root: Path) -> Path:
    return root / ".pylings" / "state.json"


def load(root: Path) -> State:
    path = _state_path(root)
    if not path.exists():
        return State()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("format_version") != FORMAT_VERSION:
            raise ValueError(
                f"unsupported state format_version: {data.get('format_version')}"
            )
        return State(completed=set(data.get("completed", [])))
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        backup = path.with_suffix(".json.bak")
        path.rename(backup)
        print(
            f"pylings: state file unreadable ({e}); backed up to {backup} "
            f"and starting fresh",
            file=sys.stderr,
        )
        return State()


def save(root: Path, state: State) -> None:
    path = _state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "format_version": FORMAT_VERSION,
        "completed": sorted(state.completed),
    }
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)


def next_pending(exercises: list, completed: set[str]) -> str | None:
    """First exercise name in `exercises` not in `completed`, or None."""
    for ex in exercises:
        if ex.name not in completed:
            return ex.name
    return None
```

- [ ] **Step 4: Update `pylings/cli.py`** — `_cmd_list` and `_cmd_reset` use the removed `state.current` / `state.next_pending`. Replace `_cmd_list` with:

```python
def _cmd_list(root: Path) -> int:
    from pylings.core.manifest import load as load_manifest
    from pylings.core.state import load as load_state, next_pending

    manifest = load_manifest(root)
    state = load_state(root)
    current = next_pending(manifest.exercises, state.completed)
    for ex in manifest.exercises:
        if ex.name in state.completed:
            marker = "✓"
        elif ex.name == current:
            marker = "●"
        else:
            marker = "🔒"
        print(f"  {marker}  {ex.topic}/{ex.name}")
    return 0
```

Replace `_cmd_reset` with (the global-cursor rewind is gone — reset just uncompletes the name):

```python
def _cmd_reset(root: Path, name: str, yes: bool) -> int:
    from pylings.core.manifest import load as load_manifest
    from pylings.core.reset import ResetError, restore
    from pylings.core.state import load as load_state, save as save_state

    manifest = load_manifest(root)
    try:
        ex = manifest.by_name(name)
    except KeyError:
        sys.stderr.write(f"pylings: no exercise named {name!r}\n")
        return 1

    if not yes:
        sys.stdout.write(f"Reset {name}? (y/N) ")
        sys.stdout.flush()
        if sys.stdin.readline().strip().lower() != "y":
            return 0

    try:
        restore(root, ex)
    except ResetError as e:
        sys.stderr.write(f"pylings: {e}\n")
        return 1

    state = load_state(root)
    state.completed.discard(name)
    save_state(root, state)
    print(f"reset: {name}")
    return 0
```

- [ ] **Step 5: Update `pylings/app.py`** — it uses `state.current`, `mark_done(name, manifest)`, `next_pending`. Make the app compute its current exercise from the flat set. Apply these edits:

In `__init__`, replace:
```python
        self.state: State = load_state(root)
        if self.state.current is None:
            self.state.current = self.state.next_pending(self.manifest)
```
with:
```python
        self.state: State = load_state(root)
        self.current: str | None = next_pending(
            self.manifest.exercises, self.state.completed
        )
```
and add the import: `from pylings.core.state import State, load as load_state, save as save_state, next_pending`.

Throughout `app.py`, replace every `self.state.current` with `self.current`. In `_apply_result`, replace `self.state.mark_done(exercise.name, self.manifest)` with:
```python
        self.state.mark_done(exercise.name)
        self.current = next_pending(self.manifest.exercises, self.state.completed)
```

- [ ] **Step 6: Update the tests that referenced the old state model**

Two existing test files reference the removed `state.current` / reset-rewind behavior:

1. `tests/tui/test_app_pilot.py` — it refers to `app.state.current`. The app now exposes the derived cursor as `app.current` (Step 5). Mechanically replace every occurrence of `app.state.current` with `app.current` in that file. (This file is fully rewritten in Task 5; this is just to keep it green in the interim.)

2. `tests/integration/test_cli_reset.py` — **delete** the two tests `test_reset_rewinds_state_when_target_precedes_current` and `test_reset_leaves_state_unchanged_when_target_is_current`. They test the global-cursor rewind, which no longer exists (and they hand-write `format_version: 1` state, which v2 now discards). Keep the other reset tests (`test_reset_restores_pristine_content_with_yes`, `test_reset_without_yes_aborts_on_no`, `test_reset_unknown_exercise_exits_nonzero`).

- [ ] **Step 7: Run the suites**

Run: `pytest tests/unit/test_state.py -q` → 7 passed.
Run: `pytest -q` → 0 failures.

- [ ] **Step 8: Commit**

```bash
git add pylings/core/state.py pylings/cli.py pylings/app.py tests/unit/test_state.py tests/tui/test_app_pilot.py tests/integration/test_cli_reset.py
git commit -m "Simplify state to a flat completed set (format_version 2)

Per-topic tracks remove the need for a single global cursor. State
keeps only the completed set; 'current' is derived via next_pending().
Old v1 state files are discarded gracefully. cli.py and app.py updated
to compute the current exercise from the flat set; the single-screen
UI behaviour is unchanged for now (the two-screen TUI lands in a later
task)."
```

---

## Task 3: CLI topic commands

Add `list <topic>`, `start <topic>`, and `verify [<topic>]`. `list` with no topic now shows topics with progress; `list <topic>` shows that topic's exercises.

**Files:**
- Modify: `pylings/cli.py`
- Test: `tests/integration/test_cli_topics.py` (new)

- [ ] **Step 1: Write the failing test** — `tests/integration/test_cli_topics.py`:

```python
# tests/integration/test_cli_topics.py
import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pylings", *args], capture_output=True, text=True
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_cli_topics.py -q`
Expected: failures (`list` doesn't take a topic; `verify` doesn't take a topic).

- [ ] **Step 3: Update `_build_parser` in `pylings/cli.py`** — give `list` and `verify` an optional `topic`, and add `start`:

```python
    p_list = sub.add_parser("list", help="List topics, or one topic's exercises.")
    p_list.add_argument("topic", nargs="?", help="Show exercises of this topic.")

    p_start = sub.add_parser("start", help="Launch the TUI on a topic's track.")
    p_start.add_argument("topic")

    p_verify = sub.add_parser(
        "verify", help="Run every exercise, or just one topic's."
    )
    p_verify.add_argument("topic", nargs="?", help="Verify only this topic.")
```

(Remove the old plain `sub.add_parser("list", ...)` and `sub.add_parser("verify", ...)` lines.)

- [ ] **Step 4: Replace `_cmd_list` and `_cmd_verify`, add a topic guard** in `pylings/cli.py`:

```python
def _resolve_topic(manifest, topic: str):
    """Return the topic name if valid, else write an error and return None."""
    if topic in manifest.topics():
        return topic
    sys.stderr.write(
        f"pylings: no topic named {topic!r}. "
        f"Topics: {', '.join(manifest.topics())}\n"
    )
    return None


def _cmd_list(root: Path, topic: str | None) -> int:
    from pylings.core.manifest import load as load_manifest
    from pylings.core.state import load as load_state, next_pending

    manifest = load_manifest(root)
    state = load_state(root)

    if topic is None:
        for name in manifest.topics():
            exs = manifest.exercises_in(name)
            done = sum(1 for ex in exs if ex.name in state.completed)
            mark = "✓" if done == len(exs) else ("●" if done else " ")
            print(f"  {mark}  {name}  {done}/{len(exs)}")
        return 0

    if _resolve_topic(manifest, topic) is None:
        return 2
    exs = manifest.exercises_in(topic)
    current = next_pending(exs, state.completed)
    for ex in exs:
        if ex.name in state.completed:
            marker = "✓"
        elif ex.name == current:
            marker = "●"
        else:
            marker = "🔒"
        print(f"  {marker}  {ex.name}")
    return 0


def _cmd_verify(root: Path, topic: str | None) -> int:
    from pylings.core.manifest import load as load_manifest
    from pylings.core.runner import run_verify

    manifest = load_manifest(root)
    if topic is not None:
        if _resolve_topic(manifest, topic) is None:
            return 2
        exercises = manifest.exercises_in(topic)
    else:
        exercises = manifest.exercises
    for ex in exercises:
        result = run_verify(ex)
        status = "✓" if result.passed else "✗"
        print(f"{status} {ex.name}")
        if not result.passed:
            sys.stderr.write(result.stderr or result.stdout)
            return 1
    return 0
```

- [ ] **Step 5: Wire the new dispatch in `main`** — replace the `verify` / `list` dispatch lines and add `start`:

```python
        if args.command == "verify":
            return _cmd_verify(args.root, args.topic)
        if args.command == "list":
            return _cmd_list(args.root, args.topic)
        if args.command == "hint":
            return _cmd_hint(args.root, args.name)
        if args.command == "run":
            return _cmd_run(args.root, args.name)
        if args.command == "reset":
            return _cmd_reset(args.root, args.name, args.yes)

        if args.command in (None, "watch", "start"):
            start_topic = getattr(args, "topic", None)
            if start_topic is not None:
                from pylings.core.manifest import load as load_manifest
                if _resolve_topic(load_manifest(args.root), start_topic) is None:
                    return 2
            from pylings.app import run_tui  # lazy: Textual is heavy
            return run_tui(args.root, start_topic)
```

`run_tui` gains an optional `start_topic` parameter — Task 5 implements it; for now update its stub signature so this compiles. In `pylings/app.py` change `def run_tui(root: Path) -> int:` to `def run_tui(root: Path, start_topic: str | None = None) -> int:` (the parameter is unused until Task 5).

- [ ] **Step 6: Replace the obsolete `test_cli_list.py`**

`tests/integration/test_cli_list.py` asserts that `pylings list` prints exercise names — but `list` now prints topics, and `list <topic>` prints exercises. `test_cli_topics.py` (Step 1) already covers both. **Delete `tests/integration/test_cli_list.py`** (`git rm tests/integration/test_cli_list.py`).

- [ ] **Step 7: Run the suites**

Run: `pytest tests/integration/test_cli_topics.py -q` → 6 passed.
Run: `pytest -q` → 0 failures.

- [ ] **Step 8: Commit**

```bash
git add pylings/cli.py pylings/app.py tests/integration/test_cli_topics.py
git add -u
git commit -m "Add topic-aware list, start, and verify to the CLI

list with no argument now shows topics with done/total progress;
list <topic> shows that topic's exercises; verify takes an optional
topic; start <topic> is accepted (the TUI honours it in a later task).
Unknown topics fail fast with the valid list."
```

---

## Task 4: Multi-topic test fixture

The TUI topic tests need a fixture with more than one topic. `tiny_curriculum` is single-topic; add a small two-topic fixture.

**Files:**
- Create: `tests/fixtures/multi_topic/info.toml`
- Create: `tests/fixtures/multi_topic/exercises/alpha/a1.py`, `a2.py`
- Create: `tests/fixtures/multi_topic/exercises/beta/b1.py`
- Create: `tests/fixtures/multi_topic/checks/alpha/a1.py`, `a2.py`
- Create: `tests/fixtures/multi_topic/checks/beta/b1.py`

- [ ] **Step 1: Create `tests/fixtures/multi_topic/info.toml`**

```toml
format_version = 1
welcome_message = "Multi-topic test fixture."
final_message = "Done."

[[exercises]]
name = "a1"
path = "exercises/alpha/a1.py"
hint = "alpha one"

[[exercises]]
name = "a2"
path = "exercises/alpha/a2.py"
hint = "alpha two"

[[exercises]]
name = "b1"
path = "exercises/beta/b1.py"
hint = "beta one"
```

- [ ] **Step 2: Create the exercise files**

`tests/fixtures/multi_topic/exercises/alpha/a1.py`:
```python
# I AM NOT DONE
x = ???
```
`tests/fixtures/multi_topic/exercises/alpha/a2.py`:
```python
# I AM NOT DONE
y = ???
```
`tests/fixtures/multi_topic/exercises/beta/b1.py`:
```python
# I AM NOT DONE
z = ???
```

- [ ] **Step 3: Create the check files**

`tests/fixtures/multi_topic/checks/alpha/a1.py`:
```python
assert x == 1
```
`tests/fixtures/multi_topic/checks/alpha/a2.py`:
```python
assert y == 2
```
`tests/fixtures/multi_topic/checks/beta/b1.py`:
```python
assert z == 3
```

- [ ] **Step 4: Sanity-check the fixture loads with two topics**

Run:
```bash
python -c "from pathlib import Path; from pylings.core.manifest import load; m = load(Path('tests/fixtures/multi_topic')); print(m.topics())"
```
Expected: `['alpha', 'beta']`

- [ ] **Step 5: Run the full suite**

Run: `pytest -q`
Expected: 0 failures (the fixture is not referenced by any test yet).

- [ ] **Step 6: Commit**

```bash
git add tests/fixtures/multi_topic
git commit -m "Add a two-topic test fixture

tiny_curriculum is single-topic and cannot exercise the topic picker
or topic grouping. multi_topic has topics alpha (2 exercises) and beta
(1), each a solvable ??? exercise with a matching check."
```

---

## Task 5: Two-screen TUI — topic picker + track

Restructure the TUI into two Textual screens: a `TopicPickerScreen` (the entry point) and a `TrackScreen` (the existing editor/auto-save loop, scoped to one topic). `PylingsApp` becomes a thin shell holding `root`, `manifest`, `state`.

**Files:**
- Create: `pylings/screens/__init__.py` (empty), `pylings/screens/topic_picker.py`, `pylings/screens/track.py`
- Rewrite: `pylings/app.py`
- Modify: `pylings/pylings.tcss`
- Rewrite: `tests/tui/test_app_pilot.py`

This is the largest task. The implementer should treat the code below as the intended design and adapt to the installed Textual (8.2.7) where an API differs — verify with the Pilot tests, never weaken an assertion.

- [ ] **Step 1: Rewrite `tests/tui/test_app_pilot.py`** (full file):

```python
# tests/tui/test_app_pilot.py
import shutil
from pathlib import Path

import pytest
from textual.widgets import TextArea
from textual.worker import WorkerCancelled

from pylings.app import PylingsApp
from pylings.screens.topic_picker import TopicPickerScreen
from pylings.screens.track import TrackScreen

MULTI = Path(__file__).parent.parent / "fixtures" / "multi_topic"


def _work_copy(tmp_path: Path) -> Path:
    work = tmp_path / "work"
    shutil.copytree(MULTI, work, ignore=shutil.ignore_patterns(".pylings"))
    return work


async def _settle(pilot) -> None:
    for _ in range(6):
        try:
            await pilot.app.workers.wait_for_complete()
        except WorkerCancelled:
            pass
        await pilot.pause()


@pytest.mark.asyncio
async def test_launches_on_topic_picker(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TopicPickerScreen)


@pytest.mark.asyncio
async def test_picker_lists_topics_with_progress(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path))
    async with app.run_test() as pilot:
        await _settle(pilot)
        rendered = " ".join(
            str(line) for line in app.screen.query(".topic-row").results()
        )
        assert "alpha" in rendered
        assert "beta" in rendered


@pytest.mark.asyncio
async def test_start_topic_opens_track(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        assert app.screen.topic == "alpha"


@pytest.mark.asyncio
async def test_f4_returns_to_picker(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path), start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        await pilot.press("f4")
        await pilot.pause()
        assert isinstance(app.screen, TopicPickerScreen)


@pytest.mark.asyncio
async def test_solving_a_topic_marks_progress(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PylingsApp(root=work, start_topic="beta")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        # beta has one exercise, b1; solve it.
        track.query_one("#code", TextArea).text = "z = 3\n"
        track._flush_and_run()
        await _settle(pilot)
        assert "b1" in app.state.completed
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/tui/test_app_pilot.py -q`
Expected: import errors / failures — `pylings.screens` does not exist yet.

- [ ] **Step 3: Create `pylings/screens/__init__.py`** — empty file.

- [ ] **Step 4: Create `pylings/screens/topic_picker.py`**

```python
# pylings/screens/topic_picker.py
from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, ListItem, ListView, Static


class TopicPickerScreen(Screen[None]):
    """Entry screen: choose a topic to work on."""

    BINDINGS = [Binding("ctrl+q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(ListView(id="topics"))
        yield Footer()

    def on_mount(self) -> None:
        self.app.title = "pylings"
        self.app.sub_title = "choose a topic"
        self._populate()

    def _populate(self) -> None:
        listview = self.query_one("#topics", ListView)
        listview.clear()
        manifest = self.app.manifest
        completed = self.app.state.completed
        for topic in manifest.topics():
            exs = manifest.exercises_in(topic)
            done = sum(1 for ex in exs if ex.name in completed)
            if done == len(exs):
                mark = "✓"
            elif done:
                mark = "●"
            else:
                mark = " "
            label = f"{mark}  {topic:<18} {done}/{len(exs)}"
            listview.append(
                ListItem(Static(label, classes="topic-row"), name=topic)
            )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        topic = event.item.name
        if topic:
            from pylings.screens.track import TrackScreen

            self.app.push_screen(TrackScreen(topic))
```

- [ ] **Step 5: Create `pylings/screens/track.py`**

This is the existing `app.py` editor/auto-save loop, moved into a `Screen` and scoped to one topic. State lives on `self.app`.

```python
# pylings/screens/track.py
from __future__ import annotations

from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Footer, Header, TextArea

from pylings.core.exercise import Exercise, RunResult
from pylings.core.runner import run as run_exercise
from pylings.core.state import next_pending, save as save_state
from pylings.widgets.editor_pane import EditorPane
from pylings.widgets.exercise_tree import ExerciseTree
from pylings.widgets.output_panel import OutputPanel
from pylings.widgets.progress import ProgressBar

_DEBOUNCE_SECONDS = 0.6


class TrackScreen(Screen[None]):
    """One topic's linear track: editor + output + auto-save loop."""

    BINDINGS = [
        Binding("f1", "toggle_hint", "Hint"),
        Binding("f2", "reset", "Reset"),
        Binding("f3", "toggle_list", "List"),
        Binding("f4", "topics", "Topics"),
        Binding("ctrl+q", "quit", "Quit"),
    ]

    def __init__(self, topic: str) -> None:
        super().__init__()
        self.topic = topic
        self._save_timer: Timer | None = None
        self._loaded_text = ""
        self.current: str | None = None

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
        self.app.sub_title = f"topic: {self.topic}"
        self.current = next_pending(self._exercises(), self.app.state.completed)
        self._render_state()
        if self.current is None:
            self.query_one(OutputPanel).show_final(
                f"Topic '{self.topic}' complete."
            )
            return
        self._load_current()
        self._run_current()
        self.query_one(EditorPane).focus_editor()

    # --- helpers ---------------------------------------------------------

    def _exercises(self) -> list[Exercise]:
        return self.app.manifest.exercises_in(self.topic)

    def _render_state(self) -> None:
        exs = self._exercises()
        done = sum(1 for ex in exs if ex.name in self.app.state.completed)
        self.query_one(ProgressBar).update_progress(done, len(exs))
        # The tree is topic-scoped: build a tiny manifest-like view.
        self.query_one(ExerciseTree).render_topic(
            self.topic, exs, self.app.state.completed, self.current
        )

    def _exercise(self, name: str) -> Exercise:
        for ex in self._exercises():
            if ex.name == name:
                return ex
        raise KeyError(name)

    def _load_current(self) -> None:
        if self.current is None:
            return
        if self._save_timer is not None:
            self._save_timer.stop()
            self._save_timer = None
        pane = self.query_one(EditorPane)
        pane.load_exercise(self._exercise(self.current))
        self._loaded_text = pane.text

    # --- auto-save / run loop -------------------------------------------

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if event.text_area is not self.query_one("#code", TextArea):
            return
        if self.query_one(EditorPane).text == self._loaded_text:
            return
        if self._save_timer is not None:
            self._save_timer.stop()
        self._save_timer = self.set_timer(_DEBOUNCE_SECONDS, self._flush_and_run)

    def _flush_and_run(self) -> None:
        self._save_timer = None
        if self.current is None:
            return
        ex = self._exercise(self.current)
        ex.path.write_text(self.query_one(EditorPane).text, encoding="utf-8")
        self._run_current()

    def _run_current(self) -> None:
        if self.current is None:
            return
        ex = self._exercise(self.current)
        self.run_worker(
            lambda: self._run_blocking(ex), exclusive=True, thread=True
        )

    def _run_blocking(self, exercise: Exercise) -> None:
        result = run_exercise(exercise)
        self.app.call_from_thread(self._apply_result, exercise, result)

    def _apply_result(self, exercise: Exercise, result: RunResult) -> None:
        if exercise.name != self.current:
            return
        self.query_one(OutputPanel).render_result(exercise, result)
        if not result.passed:
            return
        self.app.state.mark_done(exercise.name)
        save_state(self.app.root, self.app.state)
        self.current = next_pending(self._exercises(), self.app.state.completed)
        self._render_state()
        if self.current is None:
            self.query_one(OutputPanel).show_final(
                f"Topic '{self.topic}' complete — press F4 for topics."
            )
            return
        self._load_current()
        self._run_current()

    # --- actions ---------------------------------------------------------

    def action_toggle_hint(self) -> None:
        if self.current is None:
            return
        self.query_one(OutputPanel).toggle_hint(self._exercise(self.current).hint)

    def action_reset(self) -> None:
        from pylings.core.reset import restore

        if self.current is None:
            return
        if self._save_timer is not None:
            self._save_timer.stop()
            self._save_timer = None
        restore(self.app.root, self._exercise(self.current))
        self._load_current()
        self._run_current()

    def action_toggle_list(self) -> None:
        tree = self.query_one(ExerciseTree)
        tree.display = not tree.display

    def action_topics(self) -> None:
        self._flush_pending()
        self.app.pop_screen()

    def action_quit(self) -> None:
        self._flush_pending()
        self.app.exit(0)

    def _flush_pending(self) -> None:
        if self._save_timer is not None:
            self._save_timer.stop()
            self._save_timer = None
            if self.current is not None:
                self._exercise(self.current).path.write_text(
                    self.query_one(EditorPane).text, encoding="utf-8"
                )
```

- [ ] **Step 6: Add `render_topic` to `pylings/widgets/exercise_tree.py`**

The existing `ExerciseTree.render_manifest(manifest, state)` assumed a global manifest+state. Add a topic-scoped renderer alongside it (keep `render_manifest` — it is no longer called, but removing it is out of scope):

```python
    def render_topic(self, topic, exercises, completed, current) -> None:
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
```

(If `render_manifest` shares a helper, factor minimally; otherwise just add the method.)

- [ ] **Step 7: Rewrite `pylings/app.py`** (full file) — a thin shell:

```python
# pylings/app.py
from __future__ import annotations

from pathlib import Path

from textual.app import App

from pylings.core.manifest import Manifest, load as load_manifest
from pylings.core.state import State, load as load_state
from pylings.screens.topic_picker import TopicPickerScreen
from pylings.screens.track import TrackScreen


class PylingsApp(App[int]):
    CSS_PATH = "pylings.tcss"

    def __init__(self, root: Path, start_topic: str | None = None) -> None:
        super().__init__()
        self.root = root
        self.manifest: Manifest = load_manifest(root)
        self.state: State = load_state(root)
        self._start_topic = start_topic

    def on_mount(self) -> None:
        self.push_screen(TopicPickerScreen())
        if self._start_topic is not None and self._start_topic in self.manifest.topics():
            self.push_screen(TrackScreen(self._start_topic))


def run_tui(root: Path, start_topic: str | None = None) -> int:
    return PylingsApp(root, start_topic).run() or 0
```

- [ ] **Step 8: Add picker styles to `pylings/pylings.tcss`** — append:

```css
TopicPickerScreen #topics {
    padding: 1 2;
}

.topic-row {
    padding: 0 1;
}
```

- [ ] **Step 9: Run the TUI tests**

Run: `pytest tests/tui/test_app_pilot.py -q`
Expected: 5 passed. If a Textual API differs in 8.2.7 (screen stacking, `ListView` events, `query`), adapt the implementation — do not weaken the tests. If genuinely blocked, report BLOCKED.

- [ ] **Step 10: Run the full suite**

Run: `pytest -q`
Expected: 0 failures.

- [ ] **Step 11: Manual smoke test**

```bash
pylings --root tests/fixtures/multi_topic
```
Expected: a topic picker listing `alpha` and `beta`; selecting one opens its track; `F4` returns to the picker; `Ctrl+Q` quits. Do not run `pylings --root .` (it would auto-save into the real exercises).

- [ ] **Step 12: Commit**

```bash
git add pylings/app.py pylings/screens pylings/widgets/exercise_tree.py pylings/pylings.tcss tests/tui/test_app_pilot.py
git commit -m "Restructure the TUI into topic-picker and track screens

pylings now opens a topic picker; selecting a topic pushes a TrackScreen
scoped to it (the editor + auto-save loop, now per-topic). F4 returns to
the picker; finishing a topic shows a completion message. PylingsApp is
a thin shell holding root, manifest, and state. start <topic> jumps
straight into a track."
```

---

# Phase 2 — The curriculum

## Topic Authoring Procedure (shared by Tasks 6–36)

Each Phase 2 task authors **one topic**. The task entry below names the topic, its exercise count, and a per-exercise concept outline. Follow this procedure exactly.

### For each exercise N in the topic (1-indexed):

1. **Create `exercises/<topic>/<topic><N>.py`** — the broken file the learner edits:
   ```python
   # Exercise: <Topic Title> <N>
   # I AM NOT DONE
   #
   # <1-3 comment lines stating the goal precisely — the checks are hidden,
   #  so the learner must learn everything they need from this comment.>

   <broken code: a ??? placeholder, a missing line, or a wrong value>
   ```
2. **Create `checks/<topic>/<topic><N>.py`** — the hidden asserts (bare `assert`s in the exercise's namespace), ending with `print("<topic><N> ✓")`.
3. The exercise must be **broken** (its current form fails the check) and **solvable in a few lines**, covering the one concept from the outline.
4. **Difficulty ramp:** exercises 1–3 trivial (fill one value/line), 4–7 apply the concept, 8–N combine concepts into a small challenge.

### After authoring all exercises:

5. **Add one `[[exercises]]` block per exercise to `info.toml`**, in order, each with `name = "<topic><N>"`, `path = "exercises/<topic>/<topic><N>.py"`, and a one-line `hint`. Append the topic's block after the existing entries (topic order in `info.toml` is curriculum order).
6. **Verify every exercise** with this procedure (do it for each N):
   - Run the broken exercise: `pylings --root . run <topic><N>` → must exit non-zero (broken).
   - Write a correct solution into a scratch copy of the exercise file, run again → must exit 0 and print the ✓ line. Restore the broken version afterward.
   - A quick scripted way: load the manifest, apply your reference solution to a temp file, call `runner.run` on an `Exercise` pointing at it. Confirm broken-fails / solved-passes for all N.
7. **Do not leave solved exercises on disk** — every committed `exercises/<topic>/*.py` must still contain `# I AM NOT DONE` and be broken. Check with `grep -L "I AM NOT DONE" exercises/<topic>/*.py` (should print nothing).
8. **Commit**:
   ```bash
   git add exercises/<topic> checks/<topic> info.toml
   git commit -m "Add the <topic> curriculum topic

   <N> exercises covering <one-line summary>, on an easy-to-hard ramp,
   each with a hidden check. Verified: every broken form fails its check
   and a correct solution passes."
   ```

### Worked example (the `loops` topic, exercise 1)

`exercises/loops/loops1.py`:
```python
# Exercise: Loops 1
# I AM NOT DONE
#
# Use a for-loop to add the numbers 1 through 5 into `total`.

total = 0
# write your loop here
```
`checks/loops/loops1.py`:
```python
assert total == 15, "total should be 1+2+3+4+5"
print("loops1 ✓")
```
`info.toml` block:
```toml
[[exercises]]
name = "loops1"
path = "exercises/loops/loops1.py"
hint = "A for-loop over range(1, 6) accumulating into total."
```

### Notes
- Exercise files and check files carry **no `# <path>` header comment** (they are subprocess-run scripts).
- Topics with existing exercises (`variables`, `functions`) **keep** `variables1`/`variables2`/`functions1` and their checks; author the remaining exercises to reach the target count and renumber nothing.
- Keep each exercise to one concept; prefer many small exercises over few large ones.

---

## Tasks 6–36: one per topic

Each task = "author the `<topic>` topic per the Topic Authoring Procedure." The concept outline gives exercise 1..N.

### Task 6 — `variables` (10; keep existing variables1–2, add 3–10)
3 int/float/bool literals · 4 reassignment · 5 augmented assignment (`+=`) · 6 multiple assignment · 7 swapping two variables · 8 `type()` and conversion · 9 constants & naming · 10 combine: compute a result from several variables.

### Task 7 — `strings` (10)
1 create a string · 2 concatenation · 3 indexing · 4 slicing · 5 `len` and methods (`upper`/`lower`) · 6 `strip`/`replace` · 7 `split`/`join` · 8 f-strings · 9 `in` / `find` · 10 combine: format a report line.

### Task 8 — `conditionals` (10)
1 `if` · 2 `if/else` · 3 `elif` · 4 comparison operators · 5 `and`/`or` · 6 `not` · 7 nested `if` · 8 truthiness · 9 ternary expression · 10 combine: classify an input.

### Task 9 — `loops` (10)
1 `for` over `range` · 2 `for` over a list · 3 `while` · 4 accumulator · 5 `break` · 6 `continue` · 7 nested loops · 8 `enumerate` · 9 loop over a dict · 10 combine: build a list while looping.

### Task 10 — `functions` (10; keep existing functions1, add the rest)
2 define & call · 3 parameters · 4 return values · 5 default arguments · 6 keyword arguments · 7 `*args` · 8 `**kwargs` · 9 multiple return values (tuple) · 10 combine: a small helper used twice.

### Task 11 — `lists` (10)
1 create · 2 index/assign · 3 `append`/`insert` · 4 `remove`/`pop` · 5 slicing · 6 `sort`/`sorted` · 7 `len`/`in`/`count` · 8 iterate & transform · 9 nested lists · 10 combine: filter and aggregate.

### Task 12 — `tuples` (10)
1 create · 2 index · 3 unpacking · 4 single-element tuple · 5 immutability · 6 tuple in a function return · 7 swapping via tuples · 8 iterate · 9 tuple as dict key · 10 combine: process a list of tuples.

### Task 13 — `dictionaries` (10)
1 create · 2 access by key · 3 add/update · 4 `del`/`pop` · 5 `keys`/`values`/`items` · 6 `get` with default · 7 iterate · 8 `in` membership · 9 nested dict · 10 combine: count occurrences.

### Task 14 — `sets` (10)
1 create · 2 `add`/`discard` · 3 membership · 4 union · 5 intersection · 6 difference · 7 deduplicate a list · 8 subset/superset · 9 set comprehension intro · 10 combine: compare two collections.

### Task 15 — `comprehensions` (10)
1 list comprehension · 2 with a condition · 3 transform · 4 nested loop comprehension · 5 dict comprehension · 6 set comprehension · 7 comprehension over a string · 8 conditional expression inside · 9 flatten nested lists · 10 combine: build a lookup table.

### Task 16 — `exceptions` (10)
1 `try`/`except` · 2 catch a specific exception · 3 `except` with the exception object · 4 `else` clause · 5 `finally` · 6 `raise` · 7 raising with a message · 8 multiple `except` · 9 a custom exception class · 10 combine: validate input and raise.

### Task 17 — `file_io` (10)
1 write a file · 2 read a file · 3 `with` open · 4 read lines · 5 append mode · 6 iterate lines · 7 write a list of lines · 8 read then transform · 9 count words in a file · 10 combine: copy with a transformation. (Exercises create their own temp files within the script.)

### Task 18 — `classes` (13)
1 define a class · 2 `__init__` · 3 instance attributes · 4 a method · 5 `self` · 6 default attribute · 7 method using another method · 8 `__str__` · 9 `__repr__` · 10 class attribute vs instance attribute · 11 a method returning a new instance · 12 equality via `__eq__` · 13 combine: a small complete class.

### Task 19 — `functional` (10)
1 `lambda` basics · 2 `lambda` with a condition · 3 `map` · 4 `filter` · 5 `sorted` with `key` · 6 a function as an argument · 7 returning a function · 8 `functools.reduce` · 9 `any`/`all` · 10 combine: a small pipeline.

### Task 20 — `decorators` (10)
1 a function taking a function · 2 a simple decorator · 3 `@` syntax · 4 decorator preserving the return value · 5 decorator with `*args`/`**kwargs` · 6 `functools.wraps` · 7 a decorator that times/counts calls · 8 a decorator with arguments · 9 stacking two decorators · 10 combine: a memoize decorator.

### Task 21 — `generators` (10)
1 `yield` basics · 2 a generator function · 3 iterate a generator · 4 generator expression · 5 `next()` · 6 infinite generator with a guard · 7 `yield` in a loop · 8 a class with `__iter__` · 9 `__next__` · 10 combine: a streaming transformation.

### Task 22 — `context_managers` (8)
1 `with` for a file · 2 why `with` (cleanup) · 3 a class with `__enter__`/`__exit__` · 4 `__exit__` cleanup · 5 returning a value from `__enter__` · 6 `contextlib.contextmanager` · 7 suppressing with `__exit__` · 8 combine: a managed resource.

### Task 23 — `dataclasses` (8)
1 `@dataclass` basics · 2 fields with types · 3 default values · 4 `field(default_factory=...)` · 5 generated `__init__` · 6 generated `__repr__`/`__eq__` · 7 `frozen=True` · 8 combine: a dataclass with a method.

### Task 24 — `type_hints` (8)
1 annotate a variable · 2 annotate function params/return · 3 `list[int]` / `dict[str, int]` · 4 `Optional` / `| None` · 5 `tuple` types · 6 a type alias · 7 `Callable` · 8 combine: a fully-annotated function.

### Task 25 — `regex` (10)
1 `re.match` · 2 `re.search` · 3 `re.findall` · 4 character classes · 5 quantifiers · 6 anchors `^`/`$` · 7 groups · 8 `re.sub` · 9 named groups · 10 combine: extract structured data.

### Task 26 — `testing` (12)
1 a plain `assert` · 2 assert with a message · 3 write a `test_` function · 4 multiple assertions · 5 test a given function · 6 `pytest.raises` · 7 testing an exception message · 8 `pytest.mark.parametrize` (conceptually — author so the learner fills params) · 9 a fixture-style setup function · 10 testing edge cases · 11 testing a class · 12 combine: a small test suite for a given module.

### Task 27 — `recursion` (8)
1 a base case · 2 factorial · 3 sum of a list recursively · 4 countdown · 5 Fibonacci · 6 reverse a string recursively · 7 recursion over nested lists · 8 combine: a small recursive search.

### Task 28 — `modules` (8)
1 `import` a stdlib module · 2 `from ... import` · 3 `import ... as` · 4 use `math` · 5 use `random` (seeded) · 6 `__name__` · 7 the `if __name__ == "__main__"` guard · 8 combine: organise code using an import. (Where a second file is needed, the exercise creates it within the script or uses a stdlib module.)

### Task 29 — `collections` (10)
1 `Counter` basics · 2 `Counter.most_common` · 3 `defaultdict(int)` · 4 `defaultdict(list)` · 5 `namedtuple` define · 6 `namedtuple` access · 7 `deque` append/pop · 8 `deque` as a queue · 9 `Counter` arithmetic · 10 combine: tally and rank.

### Task 30 — `itertools` (8)
1 `count`/`islice` · 2 `cycle` with a guard · 3 `chain` · 4 `product` · 5 `permutations` · 6 `combinations` · 7 `groupby` · 8 combine: `accumulate` a running total.

### Task 31 — `json` (8)
1 `json.dumps` · 2 `json.loads` · 3 round-trip · 4 nested objects · 5 a list of objects · 6 `indent` formatting · 7 access nested values · 8 combine: transform a JSON document.

### Task 32 — `datetime` (8)
1 `date.today` / construct a `date` · 2 construct a `datetime` · 3 attributes (year/month/day) · 4 `timedelta` · 5 date arithmetic · 6 `strftime` formatting · 7 `strptime` parsing · 8 combine: compute a duration.

### Task 33 — `enums` (6)
1 define an `Enum` · 2 access a member · 3 `.name` / `.value` · 4 iterate members · 5 `auto()` · 6 combine: use an Enum in a function.

### Task 34 — `pathlib` (6)
1 construct a `Path` · 2 join with `/` · 3 `.name` / `.suffix` / `.stem` · 4 write and read text · 5 `exists` / `is_file` · 6 combine: build and inspect a path. (Exercises use temp paths created in the script.)

### Task 35 — `oop_advanced` (12)
1 inheritance basics · 2 calling `super().__init__` · 3 overriding a method · 4 polymorphism over a list of objects · 5 `isinstance` · 6 a `@property` getter · 7 a property setter · 8 `__len__` · 9 `__getitem__` · 10 `__eq__` and `__hash__` · 11 an abstract base class (`abc.ABC`) · 12 combine: a small class hierarchy.

### Task 36 — `async` (10)
1 an `async def` · 2 `await` · 3 `asyncio.run` · 4 `asyncio.sleep` · 5 awaiting two coroutines in sequence · 6 `asyncio.gather` · 7 creating a task · 8 an async helper returning a value · 9 an async loop · 10 combine: a small concurrent routine. (Checks call `asyncio.run` on the learner's coroutine.)

---

## Final verification (after Task 36)

- [ ] `pytest -q` — 0 failures.
- [ ] `python -X importtime -m pylings --root tests/fixtures/tiny_curriculum list 2>&1 | grep -c "import 'textual'"` — prints `0`.
- [ ] `pylings --root . list` — shows all 31 topics with `0/N` progress.
- [ ] Spot-check: `grep -rL "I AM NOT DONE" exercises/*/*.py` prints nothing (no solved exercises committed).

---

## Self-review checklist (done by the plan author, not a subagent)

- Spec coverage: per-topic model (Tasks 1–2), picker/track TUI (Task 5), CLI topic commands (Task 3), 31-topic curriculum (Tasks 6–36), testing (Tasks 1–5 + per-topic verification). ✓
- Each Phase 1 task leaves the suite green (Task 2 updates cli/app in lock-step with the state change). ✓
- Phase 2 tasks are independent and follow one fixed procedure. ✓
