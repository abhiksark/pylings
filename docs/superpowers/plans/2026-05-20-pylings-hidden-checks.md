# Pylings Hidden Checks Tree — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the `assert` checks out of the exercise files into a separate `checks/` tree that mirrors `exercises/`, so a learner only ever sees the broken code they need to fix.

**Architecture:** Each exercise becomes two files — a clean `exercises/<topic>/<name>.py` the learner edits, and a hidden `checks/<topic>/<name>.py` with the asserts. The manifest derives the check path by convention and validates it exists. The runner concatenates exercise source + check source into a temp file and runs that, so checks stay as bare asserts in the exercise's namespace.

**Tech Stack:** Python ≥ 3.11 · `tomllib` · `subprocess` · `tempfile` · pytest · Textual (TUI tests only)

**Spec:** `docs/superpowers/specs/2026-05-20-pylings-hidden-checks-design.md`

---

## File changes produced by this plan

```
pylings/
├── Readme.md                         ← MODIFY (Task 1)
├── checks/                           ← NEW tree (Task 1)
│   ├── variables/variables1.py
│   ├── variables/variables2.py
│   └── functions/functions1.py
├── exercises/
│   ├── variables/variables1.py       ← MODIFY — de-assert (Task 1)
│   ├── variables/variables2.py       ← MODIFY — de-assert (Task 1)
│   └── functions/functions1.py       ← MODIFY — de-assert (Task 1)
├── pylings/core/
│   ├── exercise.py                   ← MODIFY — add check_path (Task 3)
│   ├── manifest.py                   ← MODIFY — derive + validate (Task 3)
│   └── runner.py                     ← MODIFY — concatenate (Task 3)
└── tests/
    ├── fixtures/tiny_curriculum/
    │   ├── checks/{passing,asserts,syntax,pending}.py   ← NEW (Task 2)
    │   └── exercises/{passing,asserts,pending}.py       ← MODIFY — de-assert (Task 3)
    ├── fixtures/passing_curriculum/
    │   ├── checks/{passing1,passing2}.py                ← NEW (Task 2)
    │   └── exercises/{passing1,passing2}.py             ← MODIFY — de-assert (Task 3)
    ├── unit/{test_exercise,test_manifest,test_runner,test_reset}.py  ← MODIFY (Task 3)
    ├── tui/{test_editor_pane,test_app_pilot}.py         ← MODIFY (Task 3)
    └── integration/test_cli_verify.py                   ← MODIFY (Task 3)
```

Note: exercise files and fixture exercise/check files are subprocess-executed scripts — they do **not** carry the `# <path>` header comment. Python source/test files under `pylings/` and `tests/` do.

---

## Task 1: Migrate the real curriculum

Split each of the three real exercises: the asserts (and `variables2`'s computation scaffolding) move into a new `checks/` tree; the exercise files keep only what the learner edits, with comments that now describe the goal. Nothing in the test suite touches the real curriculum, and the runner does not yet require checks — so this task is self-contained and the suite stays green.

**Files:**
- Create: `checks/variables/variables1.py`, `checks/variables/variables2.py`, `checks/functions/functions1.py`
- Modify: `exercises/variables/variables1.py`, `exercises/variables/variables2.py`, `exercises/functions/functions1.py`
- Modify: `Readme.md`

- [ ] **Step 1: Create `checks/variables/variables1.py`**

```python
assert isinstance(a, int), "a should be an integer"
assert isinstance(b, float), "b should be a float"
assert isinstance(c, str), "c should be a string"
assert a == 0
assert b == 0.0
assert c == ""
print("variables1 ✓")
```

- [ ] **Step 2: Create `checks/variables/variables2.py`**

```python
sum_ab = a + b
diff_ab = a - b
product_ab = a * b
quotient_ab = a / b
remainder_ab = a % b
sum_ac = str(a) + c
product_ac = c * b

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

- [ ] **Step 3: Create `checks/functions/functions1.py`**

```python
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

- [ ] **Step 4: Replace `exercises/variables/variables1.py`** with the de-asserted version

```python
# Exercise: Variables 1
# ----------------------
# I AM NOT DONE
#
# Replace each ??? with a value of the right type:
#   a -> int 0,  b -> float 0.0,  c -> empty string

a = ???
b = ???
c = ???
```

- [ ] **Step 5: Replace `exercises/variables/variables2.py`** with the de-asserted version

```python
# Exercise: Variables 2
# ----------------------
# I AM NOT DONE
#
# Set a, b, c so that:
#   a + b == 13,  a - b == 7,  a * b == 30,  a % b == 1
#   str(a) + c == "10hello",  c * b == "hellohellohello"

a = ???
b = ???
c = ???
```

- [ ] **Step 6: Replace `exercises/functions/functions1.py`** with the de-asserted version

```python
# Exercise: Functions 1
# ----------------------
# I AM NOT DONE
#
# Fix the function below so it takes two numbers and returns their average.

def average():
    return (a + b) / 2
```

- [ ] **Step 7: Update `Readme.md`**

Find the `## How an exercise works` section and replace its body with:

```markdown
Each exercise is two files:
- `exercises/<topic>/<name>.py` — what you edit: a `# I AM NOT DONE` line
  near the top (the gate) and broken code to fix.
- `checks/<topic>/<name>.py` — the `assert` statements that verify your
  fix. This mirror tree is hidden; you never see or edit it.

Edit the code in the pylings editor pane. When the checks pass *and*
you've removed the `# I AM NOT DONE` line, pylings advances you to the
next exercise.
```

Find the `## Adding exercises` section and replace its body with:

```markdown
1. Create `exercises/<topic>/<name>.py` — the `# I AM NOT DONE` marker
   and the broken code.
2. Create `checks/<topic>/<name>.py` — the `assert` statements that
   verify a fix. They run in the exercise's namespace, so they can
   reference its variables and functions directly.
3. Add an entry to `info.toml`, including a `hint`.
4. The curriculum order is the order in `info.toml`.
```

- [ ] **Step 8: Verify the suite is unaffected**

Run: `pytest -q`
Expected: 0 failures (the same count as before — no test touches the real curriculum).

- [ ] **Step 9: Commit**

```bash
git add checks/ exercises/ Readme.md
git commit -m "Split the real curriculum into exercises and a checks tree

Each exercise's assert block moves into a new checks/ tree mirroring
exercises/. The exercise files now contain only the broken code and
goal-describing comments — no asserts. variables2's given computation
scaffolding moves into its check file too, so the exercise file is
just the placeholders. README updated to describe the two-file model."
```

---

## Task 2: Create check files for the test fixtures

Add a `checks/` tree to both test fixtures. This task only **creates** check files — it does not touch the fixture exercise files or any code, so nothing uses the new files yet and the suite stays green. The fixture exercise files keep their asserts for now; Task 3 de-asserts them once the runner concatenates.

**Files:**
- Create: `tests/fixtures/tiny_curriculum/checks/passing.py`, `asserts.py`, `syntax.py`, `pending.py`
- Create: `tests/fixtures/passing_curriculum/checks/passing1.py`, `passing2.py`

- [ ] **Step 1: Create `tests/fixtures/tiny_curriculum/checks/passing.py`**

```python
assert 1 + 1 == 2
print("passing ✓")
```

- [ ] **Step 2: Create `tests/fixtures/tiny_curriculum/checks/asserts.py`**

```python
assert 1 + 1 == 3, "two should equal three"
```

- [ ] **Step 3: Create `tests/fixtures/tiny_curriculum/checks/syntax.py`**

```python
# no checks — the syntax-error fixture fails in the exercise file itself
```

- [ ] **Step 4: Create `tests/fixtures/tiny_curriculum/checks/pending.py`**

```python
assert 1 + 1 == 2
print("pending tests pass")
```

- [ ] **Step 5: Create `tests/fixtures/passing_curriculum/checks/passing1.py`**

```python
assert 1 + 1 == 2
assert "hello" == "hello"
print("passing1 ✓")
```

- [ ] **Step 6: Create `tests/fixtures/passing_curriculum/checks/passing2.py`**

```python
assert add(2, 3) == 5
print("passing2 ✓")
```

- [ ] **Step 7: Verify the suite is unaffected**

Run: `pytest -q`
Expected: 0 failures (no code reads `checks/` yet).

- [ ] **Step 8: Commit**

```bash
git add tests/fixtures/tiny_curriculum/checks tests/fixtures/passing_curriculum/checks
git commit -m "Add checks/ trees to the test fixtures

Each fixture exercise gets a paired check file. The fixture exercise
files still hold their asserts for now; the runner change in the next
task is what makes these check files live, after which the fixture
exercises are de-asserted."
```

---

## Task 3: Wire up the hidden checks — model, manifest, runner, fixtures, tests

The core change: `Exercise` gains a `check_path`, the manifest derives and validates it, and the runner concatenates exercise + check. The fixture exercise files are de-asserted in the same task, and every test that constructs an `Exercise` or builds a curriculum is updated. These changes are interlocked — a required field plus the new validation plus the runner change all ripple together — so they land as one task. Do the steps in order.

**Files:**
- Modify: `pylings/core/exercise.py`, `pylings/core/manifest.py`, `pylings/core/runner.py`
- Modify: `tests/fixtures/tiny_curriculum/exercises/passing.py`, `asserts.py`, `pending.py`
- Modify: `tests/fixtures/passing_curriculum/exercises/passing1.py`, `passing2.py`
- Modify: `tests/unit/test_exercise.py`, `test_manifest.py`, `test_runner.py`, `test_reset.py`
- Modify: `tests/tui/test_editor_pane.py`, `test_app_pilot.py`
- Modify: `tests/integration/test_cli_verify.py`

- [ ] **Step 1: Add `check_path` to the `Exercise` dataclass**

Replace the `Exercise` class in `pylings/core/exercise.py` (leave `RunResult` and the file header unchanged):

```python
@dataclass(frozen=True)
class Exercise:
    name: str
    path: Path
    check_path: Path
    topic: str
    hint: str

    DONE_MARKER = "# I AM NOT DONE"

    def is_pending(self) -> bool:
        return self.DONE_MARKER in self.path.read_text(encoding="utf-8")
```

- [ ] **Step 2: Update the manifest loader**

In `pylings/core/manifest.py`, replace the `for entry in raw_exercises:` loop body with this (the surrounding `load()` function and everything else stay the same):

```python
    seen: set[str] = set()
    exercises: list[Exercise] = []
    for entry in raw_exercises:
        name = entry["name"]
        if name in seen:
            raise ManifestError(f"duplicate exercise name: {name!r}")
        seen.add(name)

        rel_path = Path(entry["path"])
        if not rel_path.parts or rel_path.parts[0] != "exercises":
            raise ManifestError(
                f"exercise path must be under exercises/: {rel_path}"
            )
        abs_path = root / rel_path
        if not abs_path.exists():
            raise ManifestError(f"exercise path does not exist: {rel_path}")

        check_rel = Path("checks", *rel_path.parts[1:])
        check_abs = root / check_rel
        if not check_abs.exists():
            raise ManifestError(f"no check file for {name!r}: {check_rel}")

        exercises.append(
            Exercise(
                name=name,
                path=abs_path,
                check_path=check_abs,
                topic=rel_path.parent.name,
                hint=entry.get("hint", ""),
            )
        )
```

- [ ] **Step 3: Update the runner to concatenate exercise + check**

Replace the `run()` function in `pylings/core/runner.py` with the version below, and add `import tempfile` to the imports at the top of the file (alongside `import os`, `import subprocess`, `import sys`, `import time`). `run_verify()` stays exactly as it is.

```python
def run(exercise: Exercise, timeout_s: float = DEFAULT_TIMEOUT_S) -> RunResult:
    """Run an exercise concatenated with its check file, in a subprocess.

    Never raises.
    """
    start = time.monotonic()
    env = {
        **os.environ,
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONIOENCODING": "utf-8",
    }
    combined = (
        exercise.path.read_text(encoding="utf-8")
        + "\n\n"
        + exercise.check_path.read_text(encoding="utf-8")
    )
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    )
    try:
        tmp.write(combined)
        tmp.close()
        try:
            proc = subprocess.run(
                [sys.executable, tmp.name],
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
            stdout = (
                e.stdout.decode("utf-8", errors="replace")
                if isinstance(e.stdout, bytes)
                else (e.stdout or "")
            )
            stderr = (
                e.stderr.decode("utf-8", errors="replace")
                if isinstance(e.stderr, bytes)
                else (e.stderr or "")
            )
            timed_out = True
    finally:
        os.unlink(tmp.name)

    passed = exit_code == 0 and not timed_out and not exercise.is_pending()

    return RunResult(
        passed=passed,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
        duration_s=duration,
        timed_out=timed_out,
    )
```

- [ ] **Step 4: De-assert the `tiny_curriculum` fixture exercises**

Replace `tests/fixtures/tiny_curriculum/exercises/passing.py` with:

```python
# passing exercise — the check verifies it
```

Replace `tests/fixtures/tiny_curriculum/exercises/asserts.py` with:

```python
# asserts exercise — the check fails on purpose
```

Replace `tests/fixtures/tiny_curriculum/exercises/pending.py` with:

```python
# I AM NOT DONE
```

Leave `tests/fixtures/tiny_curriculum/exercises/syntax.py` unchanged — its syntax error must stay in the exercise file.

- [ ] **Step 5: De-assert the `passing_curriculum` fixture exercises**

Replace `tests/fixtures/passing_curriculum/exercises/passing1.py` with:

```python
# passing1 exercise
```

Replace `tests/fixtures/passing_curriculum/exercises/passing2.py` with:

```python
def add(a, b):
    return a + b
```

- [ ] **Step 6: Rewrite `tests/unit/test_exercise.py`**

```python
# tests/unit/test_exercise.py

import dataclasses
from pathlib import Path

import pytest

from pylings.core.exercise import Exercise


def _ex(path: Path) -> Exercise:
    return Exercise(
        name="ex", path=path, check_path=path.parent / "check.py", topic="t", hint=""
    )


def test_is_pending_true_when_marker_present(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("# I AM NOT DONE\nprint('hi')\n", encoding="utf-8")
    assert _ex(file).is_pending() is True


def test_is_pending_false_when_marker_removed(tmp_path: Path) -> None:
    file = tmp_path / "ex.py"
    file.write_text("print('done')\n", encoding="utf-8")
    assert _ex(file).is_pending() is False


def test_is_pending_marker_inside_string_still_counts(tmp_path: Path) -> None:
    # Substring search is intentional — keep it simple, matches rustlings.
    file = tmp_path / "ex.py"
    file.write_text('s = "# I AM NOT DONE"\n', encoding="utf-8")
    assert _ex(file).is_pending() is True


def test_exercise_is_frozen() -> None:
    ex = Exercise(
        name="a",
        path=Path("/tmp/a.py"),
        check_path=Path("/tmp/checks/a.py"),
        topic="t",
        hint="",
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        ex.name = "b"  # type: ignore[misc]


def test_exercise_has_check_path() -> None:
    ex = Exercise(
        name="a",
        path=Path("/tmp/a.py"),
        check_path=Path("/tmp/checks/a.py"),
        topic="t",
        hint="",
    )
    assert ex.check_path == Path("/tmp/checks/a.py")
```

- [ ] **Step 7: Rewrite `tests/unit/test_manifest.py`**

```python
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
```

- [ ] **Step 8: Rewrite `tests/unit/test_runner.py`**

```python
# tests/unit/test_runner.py

from pathlib import Path

from pylings.core.exercise import Exercise
from pylings.core.runner import run

CURRICULUM = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"
EXERCISES = CURRICULUM / "exercises"
CHECKS = CURRICULUM / "checks"


def _fixture_ex(name: str) -> Exercise:
    return Exercise(
        name=name,
        path=EXERCISES / f"{name}.py",
        check_path=CHECKS / f"{name}.py",
        topic="t",
        hint="",
    )


def _tmp_ex(tmp_path: Path, exercise_src: str, check_src: str = "") -> Exercise:
    ex_path = tmp_path / "ex.py"
    check_path = tmp_path / "check.py"
    ex_path.write_text(exercise_src, encoding="utf-8")
    check_path.write_text(check_src, encoding="utf-8")
    return Exercise(
        name="ex", path=ex_path, check_path=check_path, topic="t", hint=""
    )


def test_passing_exercise_passes() -> None:
    result = run(_fixture_ex("passing"))
    assert result.passed is True
    assert result.exit_code == 0
    assert "passing" in result.stdout
    assert result.timed_out is False


def test_assertion_error_fails() -> None:
    result = run(_fixture_ex("asserts"))
    assert result.passed is False
    assert result.exit_code != 0
    assert "AssertionError" in result.stderr


def test_syntax_error_fails() -> None:
    result = run(_fixture_ex("syntax"))
    assert result.passed is False
    assert result.exit_code != 0
    assert "SyntaxError" in result.stderr


def test_failing_check_fails_a_clean_exercise(tmp_path: Path) -> None:
    # The exercise runs fine on its own; the hidden check is what fails.
    ex = _tmp_ex(tmp_path, "x = 1\n", "assert x == 2, 'x should be 2'\n")
    result = run(ex)
    assert result.passed is False
    assert "AssertionError" in result.stderr


def test_pending_marker_blocks_pass(tmp_path: Path) -> None:
    # Exit code 0 but the marker is in the exercise file → not passed.
    ex = _tmp_ex(tmp_path, "# I AM NOT DONE\n", "assert True\n")
    result = run(ex)
    assert result.exit_code == 0
    assert result.passed is False


def test_timeout(tmp_path: Path) -> None:
    ex = _tmp_ex(tmp_path, "while True:\n    pass\n")
    result = run(ex, timeout_s=0.5)
    assert result.timed_out is True
    assert result.passed is False


def test_utf8_output(tmp_path: Path) -> None:
    ex = _tmp_ex(tmp_path, "print('héllo 🐍')\n")
    result = run(ex)
    assert result.passed is True
    assert "héllo 🐍" in result.stdout
```

- [ ] **Step 9: Update `tests/unit/test_reset.py`**

Replace the `_ex` helper and the `test_snapshot_keys_on_exercise_name_not_filename` test (the rest of the file is unchanged):

Replace the helper:

```python
def _ex(tmp_path: Path, contents: str) -> Exercise:
    file = tmp_path / "ex.py"
    file.write_text(contents, encoding="utf-8")
    return Exercise(
        name="ex",
        path=file,
        check_path=tmp_path / "check.py",
        topic="t",
        hint="",
    )
```

Replace the two `Exercise(...)` constructions inside `test_snapshot_keys_on_exercise_name_not_filename`:

```python
    a = Exercise(
        name="variables_utils",
        path=a_path,
        check_path=tmp_path / "checks" / "variables_utils.py",
        topic="variables",
        hint="",
    )
    b = Exercise(
        name="functions_utils",
        path=b_path,
        check_path=tmp_path / "checks" / "functions_utils.py",
        topic="functions",
        hint="",
    )
```

- [ ] **Step 10: Update `tests/tui/test_editor_pane.py`**

In `test_load_exercise_fills_editor`, replace the `Exercise(...)` construction:

```python
    exercise = Exercise(
        name="ex",
        path=file,
        check_path=tmp_path / "check.py",
        topic="t",
        hint="",
    )
```

The other two tests in that file don't construct an `Exercise` — leave them.

- [ ] **Step 11: Update `tests/integration/test_cli_verify.py`**

Two tests build an inline curriculum and must now also write a `checks/` file. Replace `test_verify_against_only_passing_fixture` and `test_verify_ignores_marker` with:

```python
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
    (tmp_path / "exercises" / "ok.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "checks").mkdir()
    (tmp_path / "checks" / "ok.py").write_text("assert x == 1\n", encoding="utf-8")

    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 0, result.stderr


def test_verify_ignores_marker(tmp_path: Path) -> None:
    # An exercise with the marker still in place and checks passing
    # should be treated as a verify-pass.
    info = tmp_path / "info.toml"
    info.write_text(
        'format_version = 1\n'
        '[[exercises]]\nname = "ok"\npath = "exercises/ok.py"\nhint = "h"\n',
        encoding="utf-8",
    )
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "ok.py").write_text(
        "# I AM NOT DONE\nx = 1\n", encoding="utf-8"
    )
    (tmp_path / "checks").mkdir()
    (tmp_path / "checks" / "ok.py").write_text("assert x == 1\n", encoding="utf-8")

    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 0
```

Leave `test_verify_fails_on_first_failure` and `test_verify_reports_manifest_error_with_exit_2` unchanged.

- [ ] **Step 12: Update the solving-advances TUI test**

In `tests/tui/test_app_pilot.py`, replace `test_solving_advances_to_next_exercise` with a version that builds its own solvable curriculum (the `tiny_curriculum` `asserts` fixture is unsolvable by design):

```python
@pytest.mark.asyncio
async def test_solving_advances_to_next_exercise(tmp_path: Path) -> None:
    # Purpose-built solvable curriculum: one exercise, one check.
    work = tmp_path / "work"
    (work / "exercises").mkdir(parents=True)
    (work / "checks").mkdir(parents=True)
    (work / "info.toml").write_text(
        'format_version = 1\n'
        '[[exercises]]\nname = "first"\npath = "exercises/first.py"\nhint = "h"\n'
        '[[exercises]]\nname = "second"\npath = "exercises/second.py"\nhint = "h"\n',
        encoding="utf-8",
    )
    (work / "exercises" / "first.py").write_text(
        "# I AM NOT DONE\nx = ???\n", encoding="utf-8"
    )
    (work / "checks" / "first.py").write_text("assert x == 1\n", encoding="utf-8")
    (work / "exercises" / "second.py").write_text(
        "# I AM NOT DONE\ny = ???\n", encoding="utf-8"
    )
    (work / "checks" / "second.py").write_text("assert y == 2\n", encoding="utf-8")

    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert app.state.current == "first"

        # Solve `first`: correct code, marker removed.
        app.query_one("#code", TextArea).text = "x = 1\n"
        app._flush_and_run()
        await _settle(pilot)

        assert "first" in app.state.completed
        assert app.state.current == "second"
        loaded = (work / "exercises" / "second.py").read_text(encoding="utf-8")
        assert app.query_one("#code", TextArea).text == loaded
```

- [ ] **Step 13: Run the full suite**

Run: `pytest -q`
Expected: 0 failures.

If a test fails, fix the cause — do not weaken assertions. If genuinely stuck, report BLOCKED with the failing test and the symptom.

- [ ] **Step 14: Verify the curricula end-to-end**

```bash
pylings --root tests/fixtures/passing_curriculum verify
```
Expected: `✓ passing1`, `✓ passing2`, exit 0.

```bash
python -X importtime -m pylings --root tests/fixtures/tiny_curriculum list 2>&1 | grep -c "import 'textual'"
```
Expected: `0` (the cold-start guard still holds).

- [ ] **Step 15: Commit**

```bash
git add pylings/ tests/
git commit -m "Run exercises against the hidden checks tree

Exercise gains a check_path; the manifest derives it (exercises/X ->
checks/X), requires the exercise path to be under exercises/, and
validates the check file exists. The runner concatenates the exercise
and its check into a temp file and runs that. Fixture exercises are
de-asserted now that their checks live in checks/. Tests updated for
the new field, the new validation, and the concatenating runner; the
solving-advances TUI test uses a purpose-built solvable curriculum."
```

---

## Done

After Task 3:

- Opening any exercise — in the editor or on disk — shows only broken code and instructions; no `assert` statements.
- `checks/` mirrors `exercises/`; the manifest requires every exercise to have a check file.
- A run concatenates exercise + check and verifies correctness exactly as before.
- An exercise with no check file, or a path outside `exercises/`, fails manifest validation with a clear error.
- All spec success criteria are met:
  1. Exercises show only broken code — Task 1 + Task 3 (fixtures).
  2. `checks/` mirrors `exercises/` — Task 1 + Task 2.
  3. A run concatenates exercise + check — Task 3 (runner).
  4. Missing check file → `ManifestError` — Task 3 (manifest) + `test_load_rejects_missing_check_file`.
  5. Real exercises and both fixtures migrated — Tasks 1, 2, 3.
  6. Full suite green; `verify` and cold-start guard pass — Task 3, Steps 13–14.
