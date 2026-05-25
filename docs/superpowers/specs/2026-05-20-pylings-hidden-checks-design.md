# Pylings — Hidden Checks Tree Design

**Date:** 2026-05-20
**Status:** Design approved, pending implementation plan
**Owner:** abhiksark@gmail.com
**Supersedes (in part):** the single-file exercise model in `2026-05-19-pylings-rustlings-ux-design.md`

## Goal

Take the `assert` checks out of the exercise files. A learner who opens an exercise should see only the broken code they need to fix — not a wall of `assert` statements they are told not to touch. The checks move into a separate `checks/` directory tree that mirrors `exercises/` and is never shown to the learner.

## Why this matters

The single-file model (broken code + embedded asserts) put verification code directly in front of beginners. Now that the learner edits the file inside pylings' built-in editor, that `assert` block is unavoidable visual noise — intimidating and confusing for someone who just wants to set `a = 0`. Separating the checks keeps the learner's view to exactly the task.

## Non-goals

- Changing `info.toml`'s format. Check paths are derived by convention, not listed.
- Giving the learner a way to view the checks. They are hidden on purpose; a "peek" feature, if ever wanted, is a separate design.
- Touching the CLI commands, the TUI/editor, state, or reset beyond what the runner change requires.
- Reintroducing Python package structure (`__init__.py`). The chosen run model needs none.

---

## Decisions locked in during brainstorming

| Topic | Decision |
|---|---|
| Where checks live | A separate `checks/` tree mirroring `exercises/` |
| Check path | Derived by convention (`exercises/x/y.py` → `checks/x/y.py`), not listed in `info.toml` |
| How a run combines them | Concatenate exercise source + check source into a temp file, run that (Approach A) |
| Check file format | Bare `assert`s in the exercise's namespace — no imports, no boilerplate |
| `variables2` scaffolding | The given `sum_ab = a + b …` computations move to the check file; the exercise file is only the `???` placeholders |

---

## Architecture

```
pylings/
├── info.toml                         ← unchanged (check paths derived, not listed)
├── exercises/                        ← learner edits these — NO asserts
│   ├── variables/
│   │   ├── variables1.py
│   │   └── variables2.py
│   └── functions/
│       └── functions1.py
└── checks/                           ← NEW — hidden; pylings runs these
    ├── variables/
    │   ├── variables1.py
    │   └── variables2.py
    └── functions/
        └── functions1.py
```

**Path derivation.** `info.toml` lists only the exercise `path` (e.g. `exercises/variables/variables1.py`). The manifest derives the check path: drop the leading path component and re-root under `checks/`:

```
check_path = root / "checks" / Path(*Path(exercise_rel_path).parts[1:])
```

So `exercises/variables/variables1.py` → `checks/variables/variables1.py`, and `exercises/passing.py` → `checks/passing.py`.

**How a run works (Approach A).** The runner reads the exercise source and the check source, concatenates them (exercise first, then a blank line, then the check), writes a temp `.py` file, and runs `python <tempfile>`. Because the check runs in the same namespace as the exercise, check files are bare `assert`s that reference the exercise's names directly — no imports, no package machinery.

**Blast radius.** `pylings/core/{exercise,manifest,runner}.py`; the 3 real exercise files (each loses its asserts) plus 3 new check files; both test fixtures (`tiny_curriculum`, `passing_curriculum`) gain a `checks/` tree; the affected tests. The CLI commands, the TUI, the editor, `state.py`, and `reset.py` are untouched — they go through the runner or load `exercise.path`, which still points at the clean exercise file.

---

## Component changes

### `Exercise` dataclass — `pylings/core/exercise.py`

Gains one field:

```python
@dataclass(frozen=True)
class Exercise:
    name: str
    path: Path           # the exercise file the learner edits
    check_path: Path     # NEW — the hidden check file
    topic: str
    hint: str

    DONE_MARKER = "# I AM NOT DONE"

    def is_pending(self) -> bool:
        return self.DONE_MARKER in self.path.read_text(encoding="utf-8")
```

`is_pending()` still reads the *exercise* file — the `# I AM NOT DONE` marker stays there. Check files never carry the marker.

### `Manifest` loader — `pylings/core/manifest.py`

For each exercise entry, in addition to the existing validation:

- The `path` must start with `exercises/`. Otherwise raise `ManifestError` — e.g. `"exercise path must be under exercises/: <path>"`.
- Derive `check_path` per the rule above.
- The derived check file must exist on disk. Otherwise raise `ManifestError` — e.g. `"no check file for 'variables1': checks/variables/variables1.py"`.

The loader is otherwise unchanged (`format_version`, non-empty exercises, unique names, exercise path exists, default messages).

### `Runner` — `pylings/core/runner.py`

`run()` concatenates the two files and runs the combined source:

```python
def run(exercise: Exercise, timeout_s: float = DEFAULT_TIMEOUT_S) -> RunResult:
    combined = (
        exercise.path.read_text(encoding="utf-8")
        + "\n\n"
        + exercise.check_path.read_text(encoding="utf-8")
    )
    # Write `combined` to a temp .py file; run `python <tempfile>` with the
    # existing UTF-8 encoding, PYTHONDONTWRITEBYTECODE/PYTHONIOENCODING env,
    # and timeout handling; capture stdout/stderr/exit code; delete the temp
    # file in a finally block (so it is cleaned up even on TimeoutExpired).
```

- The exercise source is **first**, so a `SyntaxError`/`NameError` in the learner's code reports line numbers that match the exercise file 1:1. A *check* failure's line number is offset by the exercise's length — acceptable, because the `assert` message ("a should be an integer") carries the meaning.
- `RunResult.passed` is unchanged: `exit_code == 0 AND not timed_out AND not exercise.is_pending()`.
- `run_verify()` is unchanged in structure — it calls `run()`, then recomputes `passed` marker-agnostically.
- The temp file is created with `tempfile` and removed in a `finally` block on every path, including timeout.

### Untouched

`state.py` and `reset.py` — only exercise files are snapshotted and reset; check files are never edited. `cli.py`, `app.py`, and all widgets — they load `exercise.path` (the clean file) or call the runner.

---

## Migration

### The three real exercises

Each splits in two. The exercise file keeps only what the learner edits, plus comments that now must *describe the goal* (the learner can no longer read the asserts). The asserts — and any given verification scaffolding — move to `checks/`.

**`exercises/variables/variables1.py`:**
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
**`checks/variables/variables1.py`:**
```python
assert isinstance(a, int), "a should be an integer"
assert isinstance(b, float), "b should be a float"
assert isinstance(c, str), "c should be a string"
assert a == 0
assert b == 0.0
assert c == ""
print("variables1 ✓")
```

**`exercises/variables/variables2.py`** — the given `sum_ab = a + b …` scaffolding moves into the check file, so the exercise file is only the placeholders:
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
**`checks/variables/variables2.py`:**
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

**`exercises/functions/functions1.py`:**
```python
# Exercise: Functions 1
# ----------------------
# I AM NOT DONE
#
# Fix the function so it takes two numbers and returns their average.

def average():
    return (a + b) / 2
```
**`checks/functions/functions1.py`:**
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

`info.toml` hints are unchanged — they already describe the goal and matter more now that the asserts are hidden.

### The two test fixtures

`tiny_curriculum` and `passing_curriculum` each gain a `checks/` tree. Each fixture exercise splits so that the runner failure mode it represents still holds:

**`tests/fixtures/tiny_curriculum/`:**
| Exercise | `exercises/<name>.py` | `checks/<name>.py` | Combined behavior |
|---|---|---|---|
| `passing` | a bare comment | `assert 1 + 1 == 2` + `print("passing ✓")` | passes |
| `asserts` | a bare comment | `assert 1 + 1 == 3, "two should equal three"` | AssertionError |
| `syntax` | `def broken(:` + `    pass` | empty | SyntaxError (exercise-side, as intended) |
| `pending` | `# I AM NOT DONE` | `assert 1 + 1 == 2` + `print("pending tests pass")` | exit 0 but marker present → not passed |

**`tests/fixtures/passing_curriculum/`:** `passing1.py` and `passing2.py` split the same way — exercise file a bare comment, check file holds the original passing body.

---

## Testing

### Unit tests

- `test_exercise.py` — `Exercise` constructions add `check_path`; add a test asserting the field exists.
- `test_manifest.py` — new tests: check file missing → `ManifestError`; exercise path not under `exercises/` → `ManifestError`; `check_path` derived correctly. Existing tests use the updated `tiny_curriculum` fixture.
- `test_runner.py` — every test exercise gets a paired check file; constructions add `check_path`. Same case coverage (pass, failing check, exercise syntax error, pending marker, timeout, UTF-8), now exercised through the concatenated temp file.
- `test_state.py`, `test_reset.py` — wherever an `Exercise` is built directly, add `check_path`.

### Integration (CLI) tests

Several tests build a throwaway curriculum inline (writing an `info.toml` + an `exercises/ok.py`). Each must now also write the matching `checks/ok.py`, or the manifest rejects the curriculum.

### TUI tests

Mostly unaffected — the editor loads the clean `exercise.path`; fixture updates carry the rest. **One real change:** `test_solving_advances_to_next_exercise` currently "solves" a `tiny_curriculum` exercise by overwriting the whole file, but `tiny_curriculum`'s `asserts` fixture is unsolvable by design (its check is `assert 1 + 1 == 3`). Under the split, no exercise content can satisfy that. The test switches to a **purpose-built solvable fixture** — an inline tmp curriculum with one exercise (`# I AM NOT DONE` + `x = ???`) and a check (`assert x == 1`); the test types `x = 1`, the exercise passes, and the app advances.

### Verification

- The full suite stays green.
- `pylings --root tests/fixtures/passing_curriculum verify` exits 0.
- The cold-start guard (`hint`/`list`/`run`/`verify` never import Textual) still passes.

---

## Error handling

| Situation | Behavior |
|---|---|
| Exercise has no matching check file | `ManifestError` at startup; CLI exits 2; TUI never launches |
| Exercise `path` not under `exercises/` | `ManifestError` at startup |
| Exercise `SyntaxError` | Combined temp file fails; "Not passing yet" + traceback; line numbers match the exercise file |
| Check `AssertionError` | "Not passing yet" + the assert message; line number offset into the check region (message carries meaning) |
| Run times out | Temp file still removed via the `finally` block |

---

## Out of scope (deferred)

- A learner-facing way to view the hidden checks (a key or `pylings check <name>`). They are hidden by design.
- Listing check paths explicitly in `info.toml`. Convention-derived is simpler and matches "mirrors exercises/".
- Locking the exercise file's given scaffolding/comments as read-only. The learner can still edit anything; the comment is the only guard, as before.

---

## Success criteria

1. Opening any exercise — in the editor or on disk — shows only the broken code and its instructions; no `assert` statements.
2. The `checks/` tree mirrors `exercises/`; every exercise has a matching check file.
3. A run concatenates exercise + check and verifies correctness exactly as before.
4. An exercise with no check file fails manifest validation with a clear error.
5. The three real exercises and both test fixtures are migrated; the curriculum still works end to end.
6. The full test suite is green; `verify` and the cold-start guard still pass.
