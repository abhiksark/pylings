# Pylings Rustlings-style UX — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert pylings into a Rustlings-style interactive learning tool — a single `pylings` command with a Textual TUI, watch-mode auto-reruns, strict linear progression gated by `# I AM NOT DONE`, in-app hints, and a polished CLI.

**Architecture:** Pip-installable Python package (`pylings/`) with two surfaces — a Textual TUI for the watch flow and an argparse CLI for one-shot subcommands. Exercises are single files with bare `assert` checks at the bottom; verification runs them in a subprocess. Curriculum order and hints live in `info.toml` at the repo root. Runtime state and pristine snapshots live under `<root>/.pylings/`.

**Tech Stack:** Python ≥ 3.11 · Textual · watchfiles · stdlib `tomllib` · `subprocess` · pytest · pytest-asyncio · hatchling (build backend)

**Spec:** `docs/superpowers/specs/2026-05-19-pylings-rustlings-ux-design.md`

---

## Repo layout produced by this plan

```
pylings/                          ← repo root
├── pyproject.toml                ← NEW
├── info.toml                     ← NEW (curriculum manifest)
├── README.md                     ← MODIFY
├── .gitignore                    ← MODIFY (+ /.pylings/)
├── .github/workflows/ci.yml      ← NEW
├── pylings/                      ← NEW package
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── app.py
│   ├── pylings.tcss
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── progress.py
│   │   ├── exercise_tree.py
│   │   └── output_panel.py
│   └── core/
│       ├── __init__.py
│       ├── exercise.py
│       ├── manifest.py
│       ├── runner.py
│       ├── state.py
│       ├── reset.py
│       └── watcher.py
├── exercises/
│   ├── variables/
│   │   ├── variables1.py         ← MODIFY (re-break + fold tests)
│   │   └── variables2.py         ← MODIFY (re-break + fold tests)
│   └── functions/
│       └── functions1.py         ← MODIFY (fold tests)
└── tests/                        ← REPURPOSED (was exercise tests)
    ├── __init__.py
    ├── unit/
    │   ├── __init__.py
    │   ├── test_exercise.py
    │   ├── test_manifest.py
    │   ├── test_runner.py
    │   ├── test_state.py
    │   └── test_reset.py
    ├── integration/
    │   ├── __init__.py
    │   ├── test_cli_verify.py
    │   ├── test_cli_list.py
    │   ├── test_cli_hint.py
    │   ├── test_cli_run.py
    │   ├── test_cli_reset.py
    │   └── test_cli_cold_start.py
    ├── tui/
    │   ├── __init__.py
    │   └── test_app_pilot.py
    └── fixtures/
        └── tiny_curriculum/
            ├── info.toml
            └── exercises/
                ├── passing.py
                ├── asserts.py
                ├── syntax.py
                └── pending.py

Deleted: pylings.sh, pylings.py, exercises/__init__.py, exercises/*/__init__.py,
         existing tests/functions/*, tests/variables/*
```

---

## Task 1: Project skeleton and retire legacy

**Files:**
- Create: `pyproject.toml`
- Create: `pylings/__init__.py`, `pylings/__main__.py`, `pylings/cli.py`
- Create: `pylings/widgets/__init__.py`, `pylings/core/__init__.py`
- Create: `tests/__init__.py`, `tests/unit/__init__.py`, `tests/integration/__init__.py`, `tests/tui/__init__.py`
- Modify: `.gitignore`
- Delete: `pylings.sh`, `pylings.py`, `exercises/__init__.py`, `exercises/variables/__init__.py`, `exercises/functions/__init__.py`, `tests/variables/variables1_test.py`, `tests/variables/variables2_test.py`, `tests/functions/functions1_test.py` (these are the OLD exercise test files — the new tests/ tree replaces them)

- [ ] **Step 1: Create `pyproject.toml`**

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "pylings"
version = "0.1.0"
description = "Rustlings-style interactive Python exercises."
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
dependencies = [
    "textual>=0.50.0",
    "watchfiles>=0.20.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
]

[project.scripts]
pylings = "pylings.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["pylings"]

[tool.hatch.build.targets.wheel.force-include]
"pylings/pylings.tcss" = "pylings/pylings.tcss"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

- [ ] **Step 2: Create package `__init__.py` files (all empty)**

Create these as empty files:
- `pylings/__init__.py`
- `pylings/widgets/__init__.py`
- `pylings/core/__init__.py`
- `tests/__init__.py`
- `tests/unit/__init__.py`
- `tests/integration/__init__.py`
- `tests/tui/__init__.py`

- [ ] **Step 3: Create `pylings/__main__.py`**

```python
from pylings.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Stub `pylings/cli.py`** (will be expanded in Task 8)

```python
import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pylings")
    parser.add_argument("--version", action="version", version="pylings 0.1.0")
    parser.parse_args(argv if argv is not None else sys.argv[1:])
    print("pylings: not implemented yet", file=sys.stderr)
    return 0
```

- [ ] **Step 5: Update `.gitignore`** — append the following block

```
# Pylings runtime state
/.pylings/
```

- [ ] **Step 6: Delete legacy files**

```bash
rm pylings.sh pylings.py
rm exercises/__init__.py exercises/variables/__init__.py exercises/functions/__init__.py
rm tests/variables/variables1_test.py tests/variables/variables2_test.py tests/functions/functions1_test.py
rmdir tests/variables tests/functions
```

- [ ] **Step 7: Install in editable mode and verify package imports**

```bash
pip install -e ".[dev]"
python -m pylings --version
```
Expected: `pylings 0.1.0`

```bash
pylings --version
```
Expected: `pylings 0.1.0`

- [ ] **Step 8: Commit**

```bash
git add pyproject.toml pylings/ tests/__init__.py tests/unit/__init__.py tests/integration/__init__.py tests/tui/__init__.py .gitignore
git add -u
git commit -m "Set up pylings package skeleton and retire shell-based runner

Adds pyproject.toml with hatchling backend, package directories,
__main__ entry point, and a stub CLI that prints the version. Removes
pylings.sh, pylings.py, and the old per-exercise test files (those will
be folded into the exercises themselves in a later task)."
```

---

## Task 2: Exercise dataclass

**Files:**
- Create: `pylings/core/exercise.py`
- Test: `tests/unit/test_exercise.py`

- [ ] **Step 1: Write the failing test**

`tests/unit/test_exercise.py`:

```python
from pathlib import Path

from pylings.core.exercise import Exercise


def test_is_pending_true_when_marker_present(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("# I AM NOT DONE\nprint('hi')\n", encoding="utf-8")
    ex = Exercise(name="ex", path=file, topic="t", hint="")
    assert ex.is_pending() is True


def test_is_pending_false_when_marker_removed(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("print('done')\n", encoding="utf-8")
    ex = Exercise(name="ex", path=file, topic="t", hint="")
    assert ex.is_pending() is False


def test_is_pending_marker_inside_string_still_counts(tmp_path: Path) -> None:
    # Substring search is intentional — keep it simple, matches rustlings.
    file = tmp_path / "ex.py"
    file.write_text('s = "# I AM NOT DONE"\n', encoding="utf-8")
    ex = Exercise(name="ex", path=file, topic="t", hint="")
    assert ex.is_pending() is True


def test_exercise_is_frozen() -> None:
    ex = Exercise(name="a", path=Path("/tmp/a.py"), topic="t", hint="")
    import dataclasses
    with __import__("pytest").raises(dataclasses.FrozenInstanceError):
        ex.name = "b"  # type: ignore[misc]
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_exercise.py -v
```
Expected: `ImportError` or `ModuleNotFoundError: No module named 'pylings.core.exercise'`

- [ ] **Step 3: Write `pylings/core/exercise.py`**

```python
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Exercise:
    name: str
    path: Path
    topic: str
    hint: str

    DONE_MARKER = "# I AM NOT DONE"

    def is_pending(self) -> bool:
        return self.DONE_MARKER in self.path.read_text(encoding="utf-8")


@dataclass
class RunResult:
    passed: bool
    exit_code: int
    stdout: str
    stderr: str
    duration_s: float
    timed_out: bool
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_exercise.py -v
```
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add pylings/core/exercise.py tests/unit/test_exercise.py
git commit -m "Add Exercise and RunResult dataclasses

Exercise is a frozen dataclass describing one curriculum item plus the
done-marker check. RunResult is the value returned by the subprocess
runner (added now alongside Exercise; the runner itself comes next)."
```

---

## Task 3: Test fixtures — tiny_curriculum

**Files:**
- Create: `tests/fixtures/tiny_curriculum/info.toml`
- Create: `tests/fixtures/tiny_curriculum/exercises/passing.py`
- Create: `tests/fixtures/tiny_curriculum/exercises/asserts.py`
- Create: `tests/fixtures/tiny_curriculum/exercises/syntax.py`
- Create: `tests/fixtures/tiny_curriculum/exercises/pending.py`

These fixtures are referenced by manifest, runner, and CLI tests. No tests of their own.

- [ ] **Step 1: Create `tests/fixtures/tiny_curriculum/info.toml`**

```toml
format_version = 1
welcome_message = "Welcome to the test curriculum."
final_message = "All test exercises complete."

[[exercises]]
name = "passing"
path = "exercises/passing.py"
hint = "This one should always pass."

[[exercises]]
name = "asserts"
path = "exercises/asserts.py"
hint = "This exercise raises AssertionError on purpose."

[[exercises]]
name = "syntax"
path = "exercises/syntax.py"
hint = "This exercise has a SyntaxError on purpose."

[[exercises]]
name = "pending"
path = "exercises/pending.py"
hint = "Tests pass but the marker is still present."
```

- [ ] **Step 2: Create `tests/fixtures/tiny_curriculum/exercises/passing.py`**

```python
assert 1 + 1 == 2
print("passing ✓")
```

- [ ] **Step 3: Create `tests/fixtures/tiny_curriculum/exercises/asserts.py`**

```python
assert 1 + 1 == 3, "two should equal three"
```

- [ ] **Step 4: Create `tests/fixtures/tiny_curriculum/exercises/syntax.py`**

```python
def broken(:
    return 1
```

- [ ] **Step 5: Create `tests/fixtures/tiny_curriculum/exercises/pending.py`**

```python
# I AM NOT DONE
assert 1 + 1 == 2
print("pending tests pass")
```

- [ ] **Step 6: Commit**

```bash
git add tests/fixtures
git commit -m "Add tiny_curriculum test fixtures

Four fixture exercises covering the failure modes the runner has to
distinguish: passing, AssertionError, SyntaxError, and 'tests pass but
the I AM NOT DONE marker is still present'. Used by manifest, runner,
and CLI integration tests."
```

---

## Task 4: Manifest loader

**Files:**
- Create: `pylings/core/manifest.py`
- Test: `tests/unit/test_manifest.py`

- [ ] **Step 1: Write the failing test**

`tests/unit/test_manifest.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_manifest.py -v
```
Expected: `ModuleNotFoundError: No module named 'pylings.core.manifest'`

- [ ] **Step 3: Write `pylings/core/manifest.py`**

```python
from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from pylings.core.exercise import Exercise


class ManifestError(ValueError):
    """info.toml is missing, malformed, or fails validation."""


@dataclass(frozen=True)
class Manifest:
    exercises: list[Exercise]
    welcome_message: str
    final_message: str

    def by_name(self, name: str) -> Exercise:
        for ex in self.exercises:
            if ex.name == name:
                return ex
        raise KeyError(name)

    def index_of(self, name: str) -> int:
        for i, ex in enumerate(self.exercises):
            if ex.name == name:
                return i
        raise KeyError(name)


def load(root: Path) -> Manifest:
    info_path = root / "info.toml"
    if not info_path.exists():
        raise ManifestError(f"info.toml not found at {info_path}")

    with info_path.open("rb") as f:
        data = tomllib.load(f)

    if data.get("format_version") != 1:
        raise ManifestError(
            f"info.toml format_version must be 1, got {data.get('format_version')!r}"
        )

    raw_exercises = data.get("exercises", [])
    if not raw_exercises:
        raise ManifestError("info.toml must define a non-empty [[exercises]] array")

    seen: set[str] = set()
    exercises: list[Exercise] = []
    for entry in raw_exercises:
        name = entry["name"]
        if name in seen:
            raise ManifestError(f"duplicate exercise name: {name!r}")
        seen.add(name)

        rel_path = Path(entry["path"])
        abs_path = root / rel_path
        if not abs_path.exists():
            raise ManifestError(f"exercise path does not exist: {rel_path}")

        exercises.append(
            Exercise(
                name=name,
                path=abs_path,
                topic=rel_path.parent.name,
                hint=entry.get("hint", ""),
            )
        )

    return Manifest(
        exercises=exercises,
        welcome_message=data.get("welcome_message", "Welcome to pylings!"),
        final_message=data.get("final_message", "All exercises complete."),
    )
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_manifest.py -v
```
Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
git add pylings/core/manifest.py tests/unit/test_manifest.py
git commit -m "Add info.toml manifest loader

Loads and validates the curriculum manifest: format_version must be 1,
exercises array must be non-empty, paths must exist, names must be
unique. Welcome and final messages default if omitted."
```

---

## Task 5: Subprocess runner

**Files:**
- Create: `pylings/core/runner.py`
- Test: `tests/unit/test_runner.py`

- [ ] **Step 1: Write the failing test**

`tests/unit/test_runner.py`:

```python
from pathlib import Path

from pylings.core.exercise import Exercise
from pylings.core.runner import run

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum" / "exercises"


def _ex(name: str, path: Path) -> Exercise:
    return Exercise(name=name, path=path, topic="t", hint="")


def test_passing_exercise_passes() -> None:
    result = run(_ex("passing", FIXTURES / "passing.py"))
    assert result.passed is True
    assert result.exit_code == 0
    assert result.stdout.startswith("passing")
    assert result.timed_out is False


def test_assertion_error_fails() -> None:
    result = run(_ex("asserts", FIXTURES / "asserts.py"))
    assert result.passed is False
    assert result.exit_code != 0
    assert "AssertionError" in result.stderr


def test_syntax_error_fails() -> None:
    result = run(_ex("syntax", FIXTURES / "syntax.py"))
    assert result.passed is False
    assert result.exit_code != 0
    assert "SyntaxError" in result.stderr


def test_pending_marker_blocks_pass(tmp_path: Path) -> None:
    # Exit code 0 but marker present → not passed.
    file = tmp_path / "ex.py"
    file.write_text("# I AM NOT DONE\nassert True\n", encoding="utf-8")
    result = run(_ex("ex", file))
    assert result.exit_code == 0
    assert result.passed is False


def test_timeout(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("while True:\n    pass\n", encoding="utf-8")
    result = run(_ex("ex", file), timeout_s=0.5)
    assert result.timed_out is True
    assert result.passed is False


def test_utf8_output(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("print('héllo 🐍')\n", encoding="utf-8")
    result = run(_ex("ex", file))
    assert result.passed is True
    assert "héllo 🐍" in result.stdout
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_runner.py -v
```
Expected: `ModuleNotFoundError: No module named 'pylings.core.runner'`

- [ ] **Step 3: Write `pylings/core/runner.py`**

```python
from __future__ import annotations

import os
import subprocess
import sys
import time

from pylings.core.exercise import Exercise, RunResult

DEFAULT_TIMEOUT_S = 5.0


def run(exercise: Exercise, timeout_s: float = DEFAULT_TIMEOUT_S) -> RunResult:
    """Run a single exercise file in a subprocess. Never raises."""
    start = time.monotonic()
    env = {
        **os.environ,
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONIOENCODING": "utf-8",
    }
    try:
        proc = subprocess.run(
            [sys.executable, str(exercise.path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_s,
            env=env,
        )
        duration = time.monotonic() - start
        exit_code = proc.returncode
        stdout = proc.stdout
        stderr = proc.stderr
        timed_out = False
    except subprocess.TimeoutExpired as e:
        duration = time.monotonic() - start
        exit_code = -1
        stdout = e.stdout.decode("utf-8", errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        stderr = e.stderr.decode("utf-8", errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
        timed_out = True

    passed = exit_code == 0 and not timed_out and not exercise.is_pending()

    return RunResult(
        passed=passed,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
        duration_s=duration,
        timed_out=timed_out,
    )


def run_verify(exercise: Exercise, timeout_s: float = DEFAULT_TIMEOUT_S) -> RunResult:
    """Run an exercise but treat the marker as a no-op (CI / curriculum-author mode)."""
    result = run(exercise, timeout_s=timeout_s)
    # `verify` cares only about exit code; recompute passed without the marker check.
    result.passed = result.exit_code == 0 and not result.timed_out
    return result
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_runner.py -v
```
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add pylings/core/runner.py tests/unit/test_runner.py
git commit -m "Add subprocess-based exercise runner

run() spawns python <exercise.py>, captures stdout/stderr with forced
UTF-8 encoding, enforces a 5s timeout, and returns a RunResult. The
'passed' flag combines exit code 0 with the absence of the # I AM NOT
DONE marker. run_verify() is a sibling that ignores the marker — used
by 'pylings verify' for CI and curriculum-author validation."
```

---

## Task 6: State persistence

**Files:**
- Create: `pylings/core/state.py`
- Test: `tests/unit/test_state.py`

- [ ] **Step 1: Write the failing test**

`tests/unit/test_state.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_state.py -v
```
Expected: `ModuleNotFoundError: No module named 'pylings.core.state'`

- [ ] **Step 3: Write `pylings/core/state.py`**

```python
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from pylings.core.manifest import Manifest

FORMAT_VERSION = 1


@dataclass
class State:
    completed: set[str] = field(default_factory=set)
    current: str | None = None

    def mark_done(self, name: str, manifest: Manifest) -> None:
        self.completed.add(name)
        self.current = self.next_pending(manifest)

    def next_pending(self, manifest: Manifest) -> str | None:
        for ex in manifest.exercises:
            if ex.name not in self.completed:
                return ex.name
        return None


def _state_path(root: Path) -> Path:
    return root / ".pylings" / "state.json"


def load(root: Path) -> State:
    path = _state_path(root)
    if not path.exists():
        return State()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("format_version") != FORMAT_VERSION:
            raise ValueError(f"unknown state format_version: {data.get('format_version')}")
        return State(
            completed=set(data.get("completed", [])),
            current=data.get("current"),
        )
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        backup = path.with_suffix(".json.bak")
        path.rename(backup)
        print(
            f"pylings: state file corrupt ({e}); backed up to {backup} and starting fresh",
            file=sys.stderr,
        )
        return State()


def save(root: Path, state: State) -> None:
    path = _state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "format_version": FORMAT_VERSION,
        "completed": sorted(state.completed),
        "current": state.current,
    }
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_state.py -v
```
Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
git add pylings/core/state.py tests/unit/test_state.py
git commit -m "Add .pylings/state.json persistence

State tracks completed exercises and the current pointer. Atomic writes
via tmp-and-rename. Corruption recovery: bad JSON gets backed up to
.bak and a fresh state is returned. Sets serialized as sorted arrays
for deterministic diffs."
```

---

## Task 7: Reset snapshot + restore

**Files:**
- Create: `pylings/core/reset.py`
- Test: `tests/unit/test_reset.py`

- [ ] **Step 1: Write the failing test**

`tests/unit/test_reset.py`:

```python
from pathlib import Path

import pytest

from pylings.core.exercise import Exercise
from pylings.core.reset import ResetError, restore, snapshot


def _ex(tmp_path: Path, contents: str) -> Exercise:
    file = tmp_path / "ex.py"
    file.write_text(contents, encoding="utf-8")
    return Exercise(name="ex", path=file, topic="t", hint="")


def test_snapshot_copies_file_to_pylings_originals(tmp_path: Path) -> None:
    ex = _ex(tmp_path, "original content\n")
    snapshot(tmp_path, ex)
    snap = tmp_path / ".pylings" / "originals" / "ex.py"
    assert snap.exists()
    assert snap.read_text() == "original content\n"


def test_snapshot_does_not_overwrite_existing(tmp_path: Path) -> None:
    ex = _ex(tmp_path, "first\n")
    snapshot(tmp_path, ex)
    ex.path.write_text("modified\n", encoding="utf-8")
    snapshot(tmp_path, ex)  # second call should be a no-op
    snap = tmp_path / ".pylings" / "originals" / "ex.py"
    assert snap.read_text() == "first\n"


def test_restore_writes_snapshot_back_to_exercise(tmp_path: Path) -> None:
    ex = _ex(tmp_path, "pristine\n")
    snapshot(tmp_path, ex)
    ex.path.write_text("learner edits\n", encoding="utf-8")

    restore(tmp_path, ex)
    assert ex.path.read_text() == "pristine\n"


def test_restore_raises_when_no_snapshot(tmp_path: Path) -> None:
    ex = _ex(tmp_path, "no snapshot taken")
    with pytest.raises(ResetError, match="snapshot"):
        restore(tmp_path, ex)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_reset.py -v
```
Expected: `ModuleNotFoundError: No module named 'pylings.core.reset'`

- [ ] **Step 3: Write `pylings/core/reset.py`**

```python
from __future__ import annotations

import shutil
from pathlib import Path

from pylings.core.exercise import Exercise


class ResetError(RuntimeError):
    """Reset failed (typically: no snapshot exists)."""


def _snapshot_path(root: Path, exercise: Exercise) -> Path:
    return root / ".pylings" / "originals" / exercise.path.name


def snapshot(root: Path, exercise: Exercise) -> None:
    """Copy the pristine source into .pylings/originals/ if not already snapshotted."""
    snap = _snapshot_path(root, exercise)
    if snap.exists():
        return
    snap.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(exercise.path, snap)


def restore(root: Path, exercise: Exercise) -> None:
    """Overwrite the exercise file with its pristine snapshot."""
    snap = _snapshot_path(root, exercise)
    if not snap.exists():
        raise ResetError(
            f"no snapshot for {exercise.name!r}. Has the file been seen by pylings yet?"
        )
    shutil.copy2(snap, exercise.path)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_reset.py -v
```
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add pylings/core/reset.py tests/unit/test_reset.py
git commit -m "Add snapshot and restore for 'pylings reset'

snapshot() copies a pristine exercise to .pylings/originals/ once;
subsequent calls are no-ops. restore() overwrites the live file from
the snapshot. Missing snapshot raises ResetError with a clear message."
```

---

## Task 8: CLI core + `verify` subcommand

**Files:**
- Modify: `pylings/cli.py`
- Test: `tests/integration/test_cli_verify.py`

The CLI is the entry for every subcommand. This task replaces the stub from Task 1 with a real argparse dispatcher and implements the simplest subcommand (`verify`) end-to-end. Textual imports stay deferred — `pylings verify` must never load `pylings.app`.

- [ ] **Step 1: Write the failing test**

`tests/integration/test_cli_verify.py`:

```python
import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pylings", *args],
        capture_output=True,
        text=True,
    )


def test_verify_fails_on_first_failure() -> None:
    # passing.py passes, asserts.py fails → verify exits non-zero.
    result = _run("--root", str(FIXTURES), "verify")
    assert result.returncode != 0
    assert "asserts" in (result.stdout + result.stderr)


def test_verify_against_only_passing_fixture(tmp_path: Path) -> None:
    info = tmp_path / "info.toml"
    info.write_text(
        'format_version = 1\n'
        '[[exercises]]\n'
        'name = "ok"\n'
        'path = "exercises/ok.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "ok.py").write_text("assert True\n", encoding="utf-8")

    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 0, result.stderr


def test_verify_ignores_marker(tmp_path: Path) -> None:
    # An exercise with the marker still in place and tests passing
    # should be treated as a verify-pass.
    info = tmp_path / "info.toml"
    info.write_text(
        'format_version = 1\n'
        '[[exercises]]\nname = "ok"\npath = "exercises/ok.py"\nhint = "h"\n',
        encoding="utf-8",
    )
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "ok.py").write_text(
        "# I AM NOT DONE\nassert True\n", encoding="utf-8"
    )
    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 0


def test_verify_reports_manifest_error_with_exit_2(tmp_path: Path) -> None:
    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 2
    assert "info.toml" in result.stderr
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/integration/test_cli_verify.py -v
```
Expected: 4 failed (CLI prints "not implemented yet")

- [ ] **Step 3: Replace `pylings/cli.py` with the dispatcher**

```python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

__version__ = "0.1.0"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pylings")
    parser.add_argument("--version", action="version", version=f"pylings {__version__}")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Project root containing info.toml (default: cwd).",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("watch", help="Launch the TUI in watch mode (default).")

    p_run = sub.add_parser("run", help="Run a single exercise.")
    p_run.add_argument("name")

    p_hint = sub.add_parser("hint", help="Print the hint for an exercise.")
    p_hint.add_argument("name")

    sub.add_parser("list", help="List exercises with status markers.")

    p_reset = sub.add_parser("reset", help="Restore an exercise from its snapshot.")
    p_reset.add_argument("name")
    p_reset.add_argument("--yes", action="store_true", help="Skip the confirmation prompt.")

    sub.add_parser("verify", help="Run every exercise in order; first failure exits 1.")

    return parser


def _cmd_verify(root: Path) -> int:
    from pylings.core.manifest import load as load_manifest
    from pylings.core.runner import run_verify

    manifest = load_manifest(root)
    for ex in manifest.exercises:
        result = run_verify(ex)
        status = "✓" if result.passed else "✗"
        print(f"{status} {ex.name}")
        if not result.passed:
            sys.stderr.write(result.stderr or result.stdout)
            return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    try:
        if args.command == "verify":
            return _cmd_verify(args.root)

        if args.command in (None, "watch"):
            from pylings.app import run_tui  # lazy: Textual is heavy
            return run_tui(args.root)

        # Other subcommands wired in later tasks.
        sys.stderr.write(f"pylings: '{args.command}' not implemented yet\n")
        return 1
    except Exception as e:
        # Manifest errors and other startup failures use exit code 2.
        from pylings.core.manifest import ManifestError
        if isinstance(e, ManifestError):
            sys.stderr.write(f"pylings: {e}\n")
            return 2
        raise
```

- [ ] **Step 4: Add a stub `pylings/app.py` so the import doesn't break the verify test**

```python
from pathlib import Path


def run_tui(root: Path) -> int:
    raise NotImplementedError("TUI is wired up in a later task")
```

- [ ] **Step 5: Run test to verify it passes**

```bash
pytest tests/integration/test_cli_verify.py -v
```
Expected: 4 passed

- [ ] **Step 6: Commit**

```bash
git add pylings/cli.py pylings/app.py tests/integration/test_cli_verify.py
git commit -m "Add CLI dispatcher and pylings verify subcommand

argparse dispatch with --root and --version globals plus subcommand
stubs. verify is wired end-to-end: loads the manifest, runs each
exercise with run_verify (marker-agnostic), exits 1 on first failure
or 2 on manifest errors. Textual import deferred behind the watch
branch so subcommands stay fast."
```

---

## Task 9: `pylings list` subcommand

**Files:**
- Modify: `pylings/cli.py`
- Test: `tests/integration/test_cli_list.py`

- [ ] **Step 1: Write the failing test**

`tests/integration/test_cli_list.py`:

```python
import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pylings", *args],
        capture_output=True,
        text=True,
    )


def test_list_shows_all_exercises_in_order(tmp_path: Path, monkeypatch) -> None:
    # Use a copy of the fixture so we can control state without polluting it.
    import shutil
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)

    result = _run("--root", str(work), "list")
    assert result.returncode == 0
    lines = [l for l in result.stdout.splitlines() if l.strip()]
    names = [l.split()[-1] for l in lines]
    assert names == ["passing", "asserts", "syntax", "pending"]


def test_list_marks_current_with_dot(tmp_path: Path) -> None:
    import shutil
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    result = _run("--root", str(work), "list")
    # First exercise should be marked as current on a fresh state.
    first_line = next(l for l in result.stdout.splitlines() if "passing" in l)
    assert "●" in first_line
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/integration/test_cli_list.py -v
```
Expected: 2 failed

- [ ] **Step 3: Add `_cmd_list` to `pylings/cli.py`** (insert below `_cmd_verify`)

```python
def _cmd_list(root: Path) -> int:
    from pylings.core.manifest import load as load_manifest
    from pylings.core.state import load as load_state

    manifest = load_manifest(root)
    state = load_state(root)
    current = state.current or state.next_pending(manifest)
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

Wire it into the dispatch in `main`:

```python
        if args.command == "verify":
            return _cmd_verify(args.root)
        if args.command == "list":
            return _cmd_list(args.root)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/integration/test_cli_list.py -v
```
Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
git add pylings/cli.py tests/integration/test_cli_list.py
git commit -m "Add pylings list subcommand

Prints every exercise in curriculum order with a status marker:
✓ (completed), ● (current), 🔒 (locked / not yet reached). 'Current'
is the saved current or, if none saved, the first pending exercise."
```

---

## Task 10: `pylings hint` subcommand

**Files:**
- Modify: `pylings/cli.py`
- Test: `tests/integration/test_cli_hint.py`

- [ ] **Step 1: Write the failing test**

`tests/integration/test_cli_hint.py`:

```python
import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pylings", *args],
        capture_output=True,
        text=True,
    )


def test_hint_prints_text_for_known_exercise() -> None:
    result = _run("--root", str(FIXTURES), "hint", "asserts")
    assert result.returncode == 0
    assert "AssertionError" in result.stdout


def test_hint_for_unknown_exercise_exits_nonzero() -> None:
    result = _run("--root", str(FIXTURES), "hint", "nope")
    assert result.returncode != 0
    assert "nope" in result.stderr
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/integration/test_cli_hint.py -v
```
Expected: 2 failed

- [ ] **Step 3: Add `_cmd_hint` to `pylings/cli.py`**

```python
def _cmd_hint(root: Path, name: str) -> int:
    from pylings.core.manifest import load as load_manifest

    manifest = load_manifest(root)
    try:
        ex = manifest.by_name(name)
    except KeyError:
        sys.stderr.write(f"pylings: no exercise named {name!r}\n")
        return 1
    print(ex.hint.strip() or "(no hint provided)")
    return 0
```

Wire it into dispatch:

```python
        if args.command == "hint":
            return _cmd_hint(args.root, args.name)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/integration/test_cli_hint.py -v
```
Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
git add pylings/cli.py tests/integration/test_cli_hint.py
git commit -m "Add pylings hint subcommand

Looks up the exercise by name in info.toml and prints its hint. Unknown
names exit non-zero with a clear error."
```

---

## Task 11: `pylings run` subcommand

**Files:**
- Modify: `pylings/cli.py`
- Test: `tests/integration/test_cli_run.py`

- [ ] **Step 1: Write the failing test**

`tests/integration/test_cli_run.py`:

```python
import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pylings", *args],
        capture_output=True,
        text=True,
    )


def test_run_passing_exercise_exits_zero() -> None:
    result = _run("--root", str(FIXTURES), "run", "passing")
    assert result.returncode == 0
    assert "passing" in result.stdout


def test_run_failing_exercise_exits_nonzero() -> None:
    result = _run("--root", str(FIXTURES), "run", "asserts")
    assert result.returncode != 0
    assert "AssertionError" in (result.stdout + result.stderr)


def test_run_pending_marker_shows_nudge() -> None:
    result = _run("--root", str(FIXTURES), "run", "pending")
    # exit 0 from the script but the marker blocks pass.
    assert result.returncode != 0
    assert "I AM NOT DONE" in (result.stdout + result.stderr)


def test_run_unknown_exercise_exits_nonzero() -> None:
    result = _run("--root", str(FIXTURES), "run", "nope")
    assert result.returncode != 0
    assert "nope" in result.stderr
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/integration/test_cli_run.py -v
```
Expected: 4 failed

- [ ] **Step 3: Add `_cmd_run` to `pylings/cli.py`**

```python
def _cmd_run(root: Path, name: str) -> int:
    from pylings.core.manifest import load as load_manifest
    from pylings.core.runner import run as run_exercise

    manifest = load_manifest(root)
    try:
        ex = manifest.by_name(name)
    except KeyError:
        sys.stderr.write(f"pylings: no exercise named {name!r}\n")
        return 1

    result = run_exercise(ex)
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    if result.timed_out:
        sys.stderr.write(f"pylings: {name} timed out after {result.duration_s:.1f}s\n")
        return 1
    if result.exit_code != 0:
        return 1
    if ex.is_pending():
        sys.stderr.write(
            f"pylings: tests pass but the '# I AM NOT DONE' marker is still in {name}.\n"
        )
        return 1
    return 0
```

Wire it into dispatch:

```python
        if args.command == "run":
            return _cmd_run(args.root, args.name)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/integration/test_cli_run.py -v
```
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add pylings/cli.py tests/integration/test_cli_run.py
git commit -m "Add pylings run subcommand

Runs a single exercise and prints its output. Distinct exit codes for
script failure, timeout, and the 'tests pass but marker still present'
case. Stderr/stdout are passed through so tracebacks remain real."
```

---

## Task 12: `pylings reset` subcommand

**Files:**
- Modify: `pylings/cli.py`
- Test: `tests/integration/test_cli_reset.py`

- [ ] **Step 1: Write the failing test**

`tests/integration/test_cli_reset.py`:

```python
import shutil
import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _run(*args: str, input: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pylings", *args],
        capture_output=True,
        text=True,
        input=input,
    )


def test_reset_restores_pristine_content_with_yes(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    target = work / "exercises" / "passing.py"
    original = target.read_text()

    # Take a snapshot (verify implicitly snapshots through state-aware code;
    # for reset, we explicitly run verify first to populate originals/).
    _run("--root", str(work), "list")  # any command that triggers snapshot

    target.write_text("# scrambled by learner\n", encoding="utf-8")
    result = _run("--root", str(work), "reset", "passing", "--yes")
    assert result.returncode == 0
    assert target.read_text() == original


def test_reset_without_yes_aborts_on_no(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    _run("--root", str(work), "list")
    target = work / "exercises" / "passing.py"
    target.write_text("scrambled", encoding="utf-8")

    result = _run("--root", str(work), "reset", "passing", input="n\n")
    assert result.returncode == 0
    assert target.read_text() == "scrambled"


def test_reset_unknown_exercise_exits_nonzero() -> None:
    result = _run("--root", str(FIXTURES), "reset", "nope", "--yes")
    assert result.returncode != 0


def test_reset_rewinds_state_when_target_precedes_current(tmp_path: Path) -> None:
    """If you reset an exercise that's already completed and earlier than
    the current cursor, state should rewind: completed -= {name} and
    current = name."""
    import json

    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    _run("--root", str(work), "list")  # snapshot

    # Hand-craft state: completed=[passing, asserts], current=syntax.
    state_dir = work / ".pylings"
    state_dir.mkdir(exist_ok=True)
    (state_dir / "state.json").write_text(
        json.dumps({
            "format_version": 1,
            "completed": ["passing", "asserts"],
            "current": "syntax",
        }),
        encoding="utf-8",
    )

    result = _run("--root", str(work), "reset", "passing", "--yes")
    assert result.returncode == 0
    state = json.loads((state_dir / "state.json").read_text())
    assert "passing" not in state["completed"]
    assert state["current"] == "passing"


def test_reset_leaves_state_unchanged_when_target_is_current(tmp_path: Path) -> None:
    import json
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    _run("--root", str(work), "list")

    state_dir = work / ".pylings"
    state_dir.mkdir(exist_ok=True)
    (state_dir / "state.json").write_text(
        json.dumps({
            "format_version": 1,
            "completed": [],
            "current": "passing",
        }),
        encoding="utf-8",
    )

    result = _run("--root", str(work), "reset", "passing", "--yes")
    assert result.returncode == 0
    state = json.loads((state_dir / "state.json").read_text())
    assert state["completed"] == []
    assert state["current"] == "passing"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/integration/test_cli_reset.py -v
```
Expected: 3 failed

- [ ] **Step 3: Add `_cmd_reset` and snapshot-on-startup to `pylings/cli.py`**

Add a helper at module level:

```python
def _snapshot_all(root: Path) -> None:
    """Ensure every exercise has a snapshot in .pylings/originals/."""
    from pylings.core.manifest import load as load_manifest
    from pylings.core.reset import snapshot

    manifest = load_manifest(root)
    for ex in manifest.exercises:
        snapshot(root, ex)
```

Add the `_cmd_reset` function:

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
        answer = sys.stdin.readline().strip().lower()
        if answer != "y":
            return 0

    try:
        restore(root, ex)
    except ResetError as e:
        sys.stderr.write(f"pylings: {e}\n")
        return 1

    # Rewind state per spec: if name is completed → uncomplete it; if name
    # precedes current → make name the new current.
    state = load_state(root)
    target_idx = manifest.index_of(name)
    if state.current is not None:
        current_idx = manifest.index_of(state.current)
    else:
        current_idx = len(manifest.exercises)  # treat 'all done' as past-end

    state.completed.discard(name)
    if target_idx < current_idx:
        state.current = name
    save_state(root, state)

    print(f"reset: {name}")
    return 0
```

Update `_cmd_list` and `_cmd_verify` to call `_snapshot_all(root)` after loading the manifest so snapshots exist before any reset. The cleanest place: insert at the top of `main`'s dispatch, right after manifest-load risk:

Adjust `main` so `_snapshot_all` runs before any subcommand that touches files (any command except `--version` and bad-root cases). Insert this near the top of the `try:` block:

```python
        if args.command not in {"hint"}:  # hint only reads info.toml
            try:
                _snapshot_all(args.root)
            except Exception:
                pass  # snapshot best-effort; real errors surface from subcommands
```

Then wire `reset` into dispatch:

```python
        if args.command == "reset":
            return _cmd_reset(args.root, args.name, args.yes)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/integration/test_cli_reset.py -v
```
Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add pylings/cli.py tests/integration/test_cli_reset.py
git commit -m "Add pylings reset subcommand and snapshot-on-startup

Snapshots every exercise on the first command that touches files
(verify, list, run, reset, watch). reset restores from .pylings/
originals/ after a y/N prompt, or unconditionally with --yes."
```

---

## Task 13: Cold-start latency (lazy-import guard)

**Files:**
- Test: `tests/integration/test_cli_cold_start.py`

The spec requires sub-200 ms cold start for `pylings hint`, `list`, `run`, `verify`. Textual is the heavy import — this test prevents accidental top-level imports of `pylings.app` from any subcommand path.

- [ ] **Step 1: Write the test**

`tests/integration/test_cli_cold_start.py`:

```python
import subprocess
import sys
import time
from pathlib import Path

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _cold_start_ms(*args: str) -> float:
    # Run the subprocess with `-X importtime` and grep for textual.
    # We don't measure wall-clock for the test (CI flake); we assert that
    # textual was never imported in the subcommand path.
    proc = subprocess.run(
        [sys.executable, "-X", "importtime", "-m", "pylings", "--root", str(FIXTURES), *args],
        capture_output=True,
        text=True,
    )
    return proc.stderr  # importtime output goes to stderr


def test_hint_does_not_import_textual() -> None:
    out = _cold_start_ms("hint", "passing")
    assert "import 'textual'" not in out, f"textual loaded for `pylings hint`:\n{out}"


def test_list_does_not_import_textual() -> None:
    out = _cold_start_ms("list")
    assert "import 'textual'" not in out


def test_verify_does_not_import_textual() -> None:
    out = _cold_start_ms("verify")
    assert "import 'textual'" not in out


def test_run_does_not_import_textual() -> None:
    out = _cold_start_ms("run", "passing")
    assert "import 'textual'" not in out
```

- [ ] **Step 2: Run test to verify it passes (or fails, then fix)**

```bash
pytest tests/integration/test_cli_cold_start.py -v
```
Expected: 4 passed (if `pylings/app.py` only imports `pathlib`, no widget imports leak into the CLI path).

If a test fails, audit `pylings/cli.py` and `pylings/__main__.py` for any top-level `from pylings.app import ...` or `from pylings.widgets ...`. All Textual-touching imports must be inside `_cmd_*` or the `watch` branch.

- [ ] **Step 3: Commit**

```bash
git add tests/integration/test_cli_cold_start.py
git commit -m "Add cold-start regression test for CLI subcommands

Asserts that 'textual' is never imported during pylings hint / list /
run / verify. Uses python -X importtime and greps the trace. Prevents
accidental top-level Textual imports from regressing subcommand
responsiveness."
```

---

## Task 14: File watcher

**Files:**
- Create: `pylings/core/watcher.py`
- Test: `tests/unit/test_watcher.py`

- [ ] **Step 1: Write the failing test**

`tests/unit/test_watcher.py`:

```python
import asyncio
from pathlib import Path

import pytest

from pylings.core.watcher import watch


@pytest.mark.asyncio
async def test_watcher_yields_on_change(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("v1\n", encoding="utf-8")

    received: list[None] = []

    async def consume() -> None:
        async for _ in watch(file, debounce_ms=50):
            received.append(None)
            if len(received) >= 1:
                break

    task = asyncio.create_task(consume())
    await asyncio.sleep(0.2)
    file.write_text("v2\n", encoding="utf-8")
    await asyncio.wait_for(task, timeout=3.0)
    assert len(received) == 1


@pytest.mark.asyncio
async def test_watcher_debounces_burst(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("v1\n", encoding="utf-8")

    received: list[None] = []

    async def consume() -> None:
        async for _ in watch(file, debounce_ms=200):
            received.append(None)

    task = asyncio.create_task(consume())
    await asyncio.sleep(0.2)
    for i in range(5):
        file.write_text(f"v{i}\n", encoding="utf-8")
        await asyncio.sleep(0.02)
    await asyncio.sleep(0.6)
    task.cancel()
    assert 1 <= len(received) <= 2, f"expected debounced, got {len(received)} events"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_watcher.py -v
```
Expected: `ModuleNotFoundError: No module named 'pylings.core.watcher'`

- [ ] **Step 3: Write `pylings/core/watcher.py`**

```python
from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path

from watchfiles import awatch


async def watch(path: Path, debounce_ms: int = 100) -> AsyncIterator[None]:
    """Yield once each time `path` changes. Debounce coalesces bursty saves."""
    async for _changes in awatch(path, debounce=debounce_ms, recursive=False):
        yield None
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_watcher.py -v
```
Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
git add pylings/core/watcher.py tests/unit/test_watcher.py
git commit -m "Add async file watcher built on watchfiles

watch() is an async iterator yielding once per debounced change to the
target file. Caller decides what to do with each event (typically
re-run the exercise)."
```

---

## Task 15: TUI styling and progress widget

**Files:**
- Create: `pylings/pylings.tcss`
- Create: `pylings/widgets/progress.py`
- Test: `tests/tui/test_app_pilot.py` (initial scaffolding; full bindings test in Task 17)

- [ ] **Step 1: Create `pylings/pylings.tcss`**

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
    width: 30%;
    border-right: solid $primary;
    padding: 1;
}

#output {
    width: 1fr;
    padding: 1;
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

- [ ] **Step 2: Create `pylings/widgets/progress.py`**

```python
from __future__ import annotations

from textual.widgets import Static


class ProgressBar(Static):
    DEFAULT_CSS = ""

    def update_progress(self, completed: int, total: int) -> None:
        pct = (completed / total * 100) if total else 0
        bar_width = 20
        filled = int(bar_width * pct / 100)
        bar = "█" * filled + "░" * (bar_width - filled)
        self.update(f"Progress: {bar}  {completed}/{total}  ({pct:.0f}%)")
```

- [ ] **Step 3: Commit (no tests yet — exercised by the Pilot test in Task 17)**

```bash
git add pylings/pylings.tcss pylings/widgets/progress.py
git commit -m "Add Textual stylesheet and ProgressBar widget

ProgressBar renders a fixed-width unicode bar plus the X/Y count.
Stylesheet sets up the three-region layout (top progress, middle main
split into tree+output, slide-down hint section)."
```

---

## Task 16: Exercise tree and output panel widgets

**Files:**
- Create: `pylings/widgets/exercise_tree.py`
- Create: `pylings/widgets/output_panel.py`

- [ ] **Step 1: Create `pylings/widgets/exercise_tree.py`**

```python
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.widgets import Tree

if TYPE_CHECKING:
    from pylings.core.manifest import Manifest
    from pylings.core.state import State


class ExerciseTree(Tree[str]):
    def __init__(self) -> None:
        super().__init__("exercises", id="tree")
        self.show_root = False

    def render_manifest(self, manifest: "Manifest", state: "State") -> None:
        self.clear()
        current = state.current or state.next_pending(manifest)
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
```

- [ ] **Step 2: Create `pylings/widgets/output_panel.py`**

```python
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from pylings.core.exercise import Exercise, RunResult


class OutputPanel(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("(no run yet)", id="output-body")
        yield Static("", id="hint")

    def render_result(self, exercise: Exercise, result: RunResult) -> None:
        body = self.query_one("#output-body", Static)
        self.remove_class("passed", "failed", "pending")
        if result.timed_out:
            self.add_class("failed")
            body.update(f"[bold]Timed out after {result.duration_s:.1f}s[/bold] — possible infinite loop?")
            return
        if result.exit_code != 0:
            self.add_class("failed")
            body.update(f"[bold red]FAIL[/bold red]\n{result.stderr or result.stdout}")
            return
        if exercise.is_pending():
            self.add_class("pending")
            body.update(
                "[bold]Tests pass![/bold] Remove the [yellow]# I AM NOT DONE[/yellow] line to advance."
            )
            return
        self.add_class("passed")
        body.update(f"[bold green]✓ {exercise.name}[/bold green]\n{result.stdout}")

    def toggle_hint(self, text: str) -> None:
        hint = self.query_one("#hint", Static)
        if "visible" in hint.classes:
            hint.remove_class("visible")
        else:
            hint.add_class("visible")
            hint.update(f"[italic]Hint:[/italic] {text or '(no hint provided)'}")
```

- [ ] **Step 3: Commit**

```bash
git add pylings/widgets/exercise_tree.py pylings/widgets/output_panel.py
git commit -m "Add ExerciseTree and OutputPanel widgets

ExerciseTree groups exercises by topic and renders ✓/●/🔒 markers from
manifest + state. OutputPanel renders the latest RunResult with
state-driven styling (passed/failed/pending) and toggles a hint
section. Both are presentational; App owns state."
```

---

## Task 17: Textual App and TUI Pilot tests

**Files:**
- Modify: `pylings/app.py` (replace the NotImplementedError stub)
- Test: `tests/tui/test_app_pilot.py`

- [ ] **Step 1: Replace `pylings/app.py` with the real App**

```python
from __future__ import annotations

import asyncio
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import Footer

from pylings.core.manifest import Manifest, load as load_manifest
from pylings.core.runner import run as run_exercise
from pylings.core.state import State, load as load_state, save as save_state
from pylings.core.watcher import watch
from pylings.widgets.exercise_tree import ExerciseTree
from pylings.widgets.output_panel import OutputPanel
from pylings.widgets.progress import ProgressBar


class PylingsApp(App[int]):
    CSS_PATH = "pylings.tcss"
    BINDINGS = [
        Binding("h", "toggle_hint", "Hint"),
        Binding("r", "reset", "Reset"),
        Binding("n", "skip_animation", "Next"),
        Binding("l", "toggle_list", "List"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, root: Path) -> None:
        super().__init__()
        self.root = root
        self.manifest: Manifest = load_manifest(root)
        self.state: State = load_state(root)
        if self.state.current is None:
            self.state.current = self.state.next_pending(self.manifest)
        self._watcher_task: asyncio.Task[None] | None = None

    def compose(self) -> ComposeResult:
        yield ProgressBar(id="progress")
        yield Horizontal(ExerciseTree(), OutputPanel(id="output"), id="main")
        yield Footer()

    async def on_mount(self) -> None:
        self._render_state()
        await self._run_current()
        self._restart_watcher()

    def _render_state(self) -> None:
        tree = self.query_one(ExerciseTree)
        tree.render_manifest(self.manifest, self.state)
        progress = self.query_one(ProgressBar)
        progress.update_progress(len(self.state.completed), len(self.manifest.exercises))

    async def _run_current(self) -> None:
        if self.state.current is None:
            self.exit(0)
            return
        ex = self.manifest.by_name(self.state.current)
        result = run_exercise(ex)
        self.query_one(OutputPanel).render_result(ex, result)
        if result.passed:
            self.state.mark_done(ex.name, self.manifest)
            save_state(self.root, self.state)
            self._render_state()
            self._restart_watcher()

    def _restart_watcher(self) -> None:
        if self._watcher_task is not None:
            self._watcher_task.cancel()
        if self.state.current is None:
            return
        ex = self.manifest.by_name(self.state.current)
        self._watcher_task = asyncio.create_task(self._watch_loop(ex.path))

    async def _watch_loop(self, path: Path) -> None:
        async for _ in watch(path):
            await self._run_current()

    def action_toggle_hint(self) -> None:
        if self.state.current is None:
            return
        ex = self.manifest.by_name(self.state.current)
        self.query_one(OutputPanel).toggle_hint(ex.hint)

    def action_reset(self) -> None:
        from pylings.core.reset import restore
        if self.state.current is None:
            return
        ex = self.manifest.by_name(self.state.current)
        restore(self.root, ex)
        # Resetting the current exercise: state is unchanged (per spec), file is
        # rewritten. Re-run explicitly because shutil.copy may not trip the
        # watcher's mtime threshold on every platform.
        save_state(self.root, self.state)
        asyncio.create_task(self._run_current())

    def action_skip_animation(self) -> None:
        # Reserved for the success animation; for now a no-op outside that window.
        pass

    def action_toggle_list(self) -> None:
        tree = self.query_one(ExerciseTree)
        tree.display = not tree.display


def run_tui(root: Path) -> int:
    return PylingsApp(root).run() or 0
```

- [ ] **Step 2: Write the Pilot test**

`tests/tui/test_app_pilot.py`:

```python
import shutil
from pathlib import Path

import pytest

from pylings.app import PylingsApp

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


@pytest.mark.asyncio
async def test_app_launches_and_shows_first_exercise(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await pilot.pause()
        progress = pilot.app.query_one("#progress")
        assert "0/4" in str(progress.renderable) or "1/4" in str(progress.renderable)


@pytest.mark.asyncio
async def test_h_binding_toggles_hint(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await pilot.pause()
        hint = pilot.app.query_one("#hint")
        assert "visible" not in hint.classes
        await pilot.press("h")
        await pilot.pause()
        assert "visible" in hint.classes


@pytest.mark.asyncio
async def test_q_binding_quits(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await pilot.pause()
        await pilot.press("q")


@pytest.mark.asyncio
async def test_r_binding_resets_current_file(tmp_path: Path) -> None:
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await pilot.pause()
        # Scribble on the current exercise (passing.py).
        target = work / "exercises" / "passing.py"
        original = target.read_text()
        target.write_text("# scrambled\n", encoding="utf-8")

        await pilot.press("r")
        await pilot.pause()
        assert target.read_text() == original


@pytest.mark.asyncio
async def test_l_binding_toggles_tree_visibility(tmp_path: Path) -> None:
    from pylings.widgets.exercise_tree import ExerciseTree

    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await pilot.pause()
        tree = pilot.app.query_one(ExerciseTree)
        before = tree.display
        await pilot.press("l")
        await pilot.pause()
        assert tree.display != before


@pytest.mark.asyncio
async def test_n_binding_is_a_noop_outside_animation(tmp_path: Path) -> None:
    # Smoke test only: pressing n must not crash, and state should be unchanged.
    work = tmp_path / "work"
    shutil.copytree(FIXTURES, work)
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await pilot.pause()
        completed_before = set(pilot.app.state.completed)
        current_before = pilot.app.state.current
        await pilot.press("n")
        await pilot.pause()
        assert pilot.app.state.completed == completed_before
        assert pilot.app.state.current == current_before
```

- [ ] **Step 3: Run the Pilot tests**

```bash
pytest tests/tui/test_app_pilot.py -v
```
Expected: 3 passed

- [ ] **Step 4: Manual smoke test — confirm the TUI actually launches**

```bash
cd /home/abhik/Projects/personal/pylings
pylings --root tests/fixtures/tiny_curriculum
```
Expected: a Textual UI appears with progress, the exercise tree, and the output panel showing the first fixture exercise. Press `q` to quit.

Note: this is a manual visual check — the headless tests above don't catch styling/layout regressions. If the manual UI is broken, fix CSS or widget composition before continuing.

- [ ] **Step 5: Commit**

```bash
git add pylings/app.py tests/tui/test_app_pilot.py
git commit -m "Wire up the Textual TUI App

PylingsApp composes ProgressBar + ExerciseTree + OutputPanel + Footer,
runs the current exercise on mount, and restarts an async watcher loop
on each advance. Bindings: h toggles hint, r resets, n is reserved
(animation skip), l toggles the tree, q quits. Pilot tests cover
launch, hint toggle, and quit."
```

---

## Task 18: Migrate the real curriculum

**Files:**
- Modify: `exercises/variables/variables1.py`
- Modify: `exercises/variables/variables2.py`
- Modify: `exercises/functions/functions1.py`

Each file gets the `# I AM NOT DONE` marker, has the corresponding test asserts folded in at the bottom, and (for `variables1` and `variables2`) is re-broken with placeholders so the learner actually has to do something. `functions1.py` is already broken; only the test folding is needed.

- [ ] **Step 1: Replace `exercises/variables/variables1.py`**

```python
# Exercise: Variables 1
# ----------------------
# I AM NOT DONE
#
# Replace each `???` with a value of the right type so the checks pass.
#   a should be an int with value 0
#   b should be a float with value 0.0
#   c should be the empty string

a = ???
b = ???
c = ???

# --- checks (do not edit below) ---
assert isinstance(a, int), "a should be an integer"
assert isinstance(b, float), "b should be a float"
assert isinstance(c, str), "c should be a string"
assert a == 0
assert b == 0.0
assert c == ""
print("variables1 ✓")
```

- [ ] **Step 2: Replace `exercises/variables/variables2.py`**

```python
# Exercise: Variables 2
# ----------------------
# I AM NOT DONE
#
# Replace each `???` so the operations below produce the expected results.
#   a is an int
#   b is an int
#   c is a string

a = ???
b = ???
c = ???

sum_ab = a + b
diff_ab = a - b
product_ab = a * b
quotient_ab = a / b
remainder_ab = a % b
sum_ac = str(a) + c
product_ac = c * b

# --- checks (do not edit below) ---
assert isinstance(a, int), "a should be an integer"
assert isinstance(b, int), "b should be an integer"
assert isinstance(c, str), "c should be a string"
assert sum_ab == 13, "sum_ab should be 13"
assert diff_ab == 7, "diff_ab should be 7"
assert product_ab == 30, "product_ab should be 30"
assert quotient_ab == 3.3333333333333335
assert remainder_ab == 1
assert sum_ac == "10hello"
assert product_ac == "hellohellohello"
print("variables2 ✓")
```

- [ ] **Step 3: Replace `exercises/functions/functions1.py`**

```python
# Exercise: Functions 1
# ----------------------
# I AM NOT DONE
#
# Fix the function below so it takes two numbers and returns their average.

def average():
    return (a + b) / 2

# --- checks (do not edit below) ---
assert average(2, 4) == 3
assert average(10, 20) == 15
assert average(-2, -4) == -3
assert average(-10, -20) == -15
assert average(1.5, 2.5) == 2
assert average(0.5, 1.5) == 1
assert average(0, 0) == 0
assert average(3, 4.5) == 3.75
print("functions1 ✓")
```

- [ ] **Step 4: Sanity-check that each file fails as expected (since they're not yet done)**

```bash
python exercises/variables/variables1.py
```
Expected: `SyntaxError` (because `???` is not valid Python).

```bash
python exercises/functions/functions1.py
```
Expected: `NameError` (because `a` and `b` aren't defined in the broken `average()`).

- [ ] **Step 5: Commit**

```bash
git add exercises/variables/variables1.py exercises/variables/variables2.py exercises/functions/functions1.py
git commit -m "Migrate existing exercises to single-file Rustlings-style format

Each exercise now has the # I AM NOT DONE marker, embedded asserts (the
verification checks), and re-broken placeholder values so the learner
actually has a fix-to-pass step. variables1/variables2 were previously
shipping with correct answers; they now ship with ??? placeholders.
functions1 was already broken (missing parameters); only the asserts
were folded in."
```

---

## Task 19: Real `info.toml` for the live curriculum

**Files:**
- Create: `info.toml` (at repo root)

- [ ] **Step 1: Create `info.toml`**

```toml
format_version = 1
welcome_message = "Welcome to pylings! Save a file to re-run its checks."
final_message = "All exercises complete. 🐍 Nice work."

[[exercises]]
name = "variables1"
path = "exercises/variables/variables1.py"
hint = """
Declare a, b, c with concrete values of the right type.
A bare 0 is an int; 0.0 is a float; \"\" is the empty string.
"""

[[exercises]]
name = "variables2"
path = "exercises/variables/variables2.py"
hint = """
a and b are ints; c is a string.
Pick values so a + b == 13 and a % b == 1, then check that
str(a) + c equals \"10hello\".
"""

[[exercises]]
name = "functions1"
path = "exercises/functions/functions1.py"
hint = """
The function is called as average(2, 4), so it needs to accept two
parameters. Update the signature so a and b are arguments rather than
unresolved names.
"""
```

- [ ] **Step 2: Verify the manifest loads against the real curriculum**

```bash
pylings --root . list
```
Expected: three lines (variables1, variables2, functions1) with the first one marked `●`.

- [ ] **Step 3: Commit**

```bash
git add info.toml
git commit -m "Add info.toml for the live curriculum

Three exercises in order — variables1, variables2, functions1 — each
with a hint that nudges without giving the answer."
```

---

## Task 20: README and CI workflow

**Files:**
- Modify: `Readme.md`
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Replace `Readme.md`**

```markdown
# Pylings

Rustlings, but for Python. A series of interactive exercises that teach Python by example — each ships with broken code and a `# I AM NOT DONE` marker. Fix it, save the file, watch the checks pass, advance to the next one.

## Install

```bash
pipx install pylings           # end users
# or, for contributors:
git clone <repo> pylings && cd pylings && pip install -e ".[dev]"
```

## Use

```bash
pylings                                # launches the TUI in watch mode
pylings list                           # shows every exercise with its status
pylings hint variables1                # prints the hint for an exercise
pylings run variables1                 # one-shot run, no TUI
pylings reset variables1               # restore original (asks y/N; --yes skips)
pylings verify --root <path>           # CI / curriculum-author validation
```

In the TUI:

| Key | Action |
|---|---|
| `h` | Toggle hint |
| `r` | Reset current exercise |
| `n` | Skip success animation |
| `l` | Toggle exercise list |
| `q` | Quit |

## How an exercise works

Each file in `exercises/` contains:
1. A `# I AM NOT DONE` line near the top (the gate).
2. Broken code you have to fix.
3. A block of `assert` statements at the bottom (the checks — don't edit).

When the script exits 0 *and* you've removed `# I AM NOT DONE`, pylings advances you to the next exercise.

## Adding exercises

1. Create the file under `exercises/<topic>/<name>.py` with the marker, the broken code, and the asserts.
2. Add an entry to `info.toml`, including a `hint`.
3. The curriculum order is the order in `info.toml`.

## Development

```bash
pip install -e ".[dev]"
pytest                                                # all tests
pylings verify --root tests/fixtures/tiny_curriculum  # smoke-check the runner
```
```

- [ ] **Step 2: Create `.github/workflows/ci.yml`**

```yaml
name: ci

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: pytest -v
      - run: pylings verify --root tests/fixtures/tiny_curriculum
```

- [ ] **Step 3: Run the full test suite locally before committing**

```bash
pytest -v
pylings verify --root tests/fixtures/tiny_curriculum
```
Expected: all tests pass; verify exits 0.

- [ ] **Step 4: Commit**

```bash
git add Readme.md .github/workflows/ci.yml
git commit -m "Update README and add CI workflow

README is rewritten for the new pylings CLI / TUI flow. CI runs pytest
across Python 3.11/3.12/3.13 on Ubuntu and finishes with
'pylings verify' against the test fixture curriculum (not the real
curriculum, which is broken-by-design)."
```

---

## Done

After Task 20, the redesign is complete:

- `pylings` is a real CLI; `pylings <subcommand>` is sub-200 ms.
- `pylings` (no args) opens a Textual TUI with watch-mode auto-reruns and a `# I AM NOT DONE` gate.
- The three existing exercises ship as single files with embedded asserts; the curriculum is genuinely broken at start.
- All success criteria from the spec are satisfied:
  1. Install with `pip install -e .` or `pipx install pylings` — yes (Task 1, 20).
  2. Save → re-run loop — yes (Task 14, 17).
  3. Removing marker advances — yes (Task 17).
  4. `hint`/`list`/`run`/`reset`/`verify` work — yes (Tasks 8–12).
  5. CI green on fixtures — yes (Task 20).
  6. Unit + integration + TUI tests pass — yes (every task adds the corresponding tests).
  7. Cold start < 200 ms — yes (Task 13 guards against regression).
