# Pylings — Rustlings-style UX Redesign

**Date:** 2026-05-19
**Status:** Design approved, pending implementation plan
**Owner:** abhiksark@gmail.com

## Goal

Turn pylings from a shell-driven, sequential test runner into a Rustlings-style interactive learning tool that is genuinely easy for Python beginners to use. The redesigned tool exposes a single `pylings` command that launches a Textual TUI with a watch loop, strict linear progression, an `# I AM NOT DONE` gate, in-app hints, and a polished progress display.

## Non-goals

- Replacing pytest as the test framework for *pylings itself*. (Pytest stays — for testing the runner, not the exercises.)
- Authoring new exercise content. Curriculum expansion is a follow-up.
- Web or GUI front-ends. Terminal-only.
- Windows-first polish. Linux/macOS are the primary targets; Windows should work but isn't a CI matrix entry initially.

## Why this matters

The current pylings (`pylings.sh` + split `exercises/` and `tests/` trees) works but has none of the affordances that make Rustlings beloved: no watch loop, no progression gate, no hints, no progress indicator, no single-binary feel. Learners get a wall of pytest output and must shuttle between two file trees. This redesign closes that gap.

---

## Decisions locked in during brainstorming

| Topic | Decision |
|---|---|
| Ambition level | Full port — TUI + watch + hints + gating |
| Exercise file model | Single file per exercise (bare `assert`s at the bottom) |
| Progression | Strict linear; next exercise locked until current passes AND `# I AM NOT DONE` is removed |
| Metadata location | Single `info.toml` at project root |
| TUI library | Textual |
| Distribution | pip-installable package + `python -m pylings` for contributors |
| Verifier | Subprocess per run (Approach A): `python <exercise.py>` |

---

## Architecture

### Repo layout

```
pylings/                          ← repo root
├── pyproject.toml                ← `pylings` console-script entry point
├── info.toml                     ← exercise order + hints (rustlings-style)
├── README.md
├── pylings/                      ← the Python package
│   ├── __init__.py
│   ├── __main__.py               ← enables `python -m pylings`
│   ├── cli.py                    ← argparse → subcommands or TUI
│   ├── app.py                    ← Textual App (watch/TUI mode)
│   ├── pylings.tcss              ← Textual stylesheet
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── exercise_tree.py      ← left pane: tree w/ ✓/●/🔒 markers
│   │   ├── output_panel.py       ← right pane: test output + hint
│   │   └── progress.py           ← top bar: X/Y, %
│   └── core/
│       ├── __init__.py
│       ├── exercise.py           ← Exercise dataclass + done-marker helpers
│       ├── manifest.py           ← tomllib loader for info.toml
│       ├── runner.py             ← subprocess runner
│       ├── watcher.py            ← watchfiles wrapper
│       ├── state.py              ← .pylings/state.json persistence
│       └── reset.py              ← restore from .pylings/originals/
├── exercises/                    ← the curriculum (single-file model)
│   ├── variables/
│   ├── functions/
│   └── …
├── .pylings/                     ← gitignored runtime dir
│   ├── state.json                ← progress
│   └── originals/                ← pristine copies for `pylings reset`
└── tests/                        ← unit/integration tests of pylings ITSELF
    ├── unit/
    ├── integration/
    ├── tui/
    └── fixtures/
        └── tiny_curriculum/
```

### Dependencies

- Python ≥ 3.11 (for stdlib `tomllib`)
- `textual` — TUI framework
- `watchfiles` — file watcher (used by Textual ecosystem as well)
- `rich` — pulled in transitively by Textual; used directly for syntax-highlighted tracebacks

Dev-only: `pytest`, `pytest-asyncio`.

### Migration of existing content

1. Each exercise in `exercises/<topic>/<name>.py` absorbs its corresponding `tests/<topic>/<name>_test.py` content as bottom-of-file `assert` statements.
2. The old `tests/` tree is emptied and repurposed for tests of pylings itself.
3. `pylings.sh` is deleted. The README is updated to direct CI/script callers to `pylings verify` instead.
4. `pylings.py` (currently empty) is deleted — superseded by the package.
5. Each exercise file gains an `# I AM NOT DONE` line near the top. Existing inconsistent markers (`# notdone`, `# not done`) are normalized.

---

## Core data model

```python
# pylings/core/exercise.py
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Exercise:
    name: str          # "variables1"
    path: Path         # exercises/variables/variables1.py
    topic: str         # "variables" (derived from path parent)
    hint: str          # from info.toml

    DONE_MARKER = "# I AM NOT DONE"

    def is_pending(self) -> bool:
        return self.DONE_MARKER in self.path.read_text(encoding="utf-8")


@dataclass
class RunResult:
    passed: bool       # exit 0 AND not pending
    exit_code: int
    stdout: str
    stderr: str
    duration_s: float
    timed_out: bool
```

---

## Components

| Module | Responsibility | Key API |
|---|---|---|
| `core/manifest.py` | Parse `info.toml`, validate every exercise path exists, return ordered `list[Exercise]`. | `load(root: Path) -> Manifest` |
| `core/runner.py` | Spawn `python <path>` with 5 s timeout, capture streams. Never raises — all failure encoded in `RunResult`. | `run(ex: Exercise) -> RunResult` |
| `core/state.py` | Atomic read/write of `.pylings/state.json`. Holds `{completed: set[str], current: str | None}`. | `load()`, `mark_done(name)`, `next_pending(manifest)` |
| `core/reset.py` | On first observation of an exercise, snapshot to `.pylings/originals/`. `reset(name)` copies snapshot back. | `snapshot(ex)`, `restore(ex)` |
| `core/watcher.py` | `async for changes in awatch(path)` → debounced 100 ms → yield. | `watch(path) -> AsyncIterator[None]` |
| `app.py` | Textual `App`; wires widgets + watcher + runner + state. | `PylingsApp(root).run()` |
| `widgets/*` | Pure presentation. Receive events, render. | — |
| `cli.py` | argparse dispatch to TUI or one-shot subcommands. | `main(argv)` |

### CLI surface

| Command | Behavior |
|---|---|
| `pylings` (no args) | Launch TUI in watch mode on the current pending exercise |
| `pylings watch` | Explicit form of the above |
| `pylings run <name>` | One-shot run; prints result; exits 0/1 |
| `pylings hint <name>` | Prints hint from `info.toml` to stdout |
| `pylings list` | Prints all exercises with ✓/●/🔒 markers |
| `pylings reset <name> [--yes]` | Restore from `.pylings/originals/`. Confirms unless `--yes` |
| `pylings verify` | Run every exercise in order; first failure exits 1. CI-friendly. |

### TUI bindings (Textual `Footer`)

| Key | Action |
|---|---|
| `h` | Toggle hint pane |
| `r` | Reset current exercise (with `y/N` modal) |
| `n` | Advance to next pending (only enabled when current is done) |
| `l` | Toggle list view of all exercises |
| `q` | Quit |

---

## `info.toml` format

```toml
format_version = 1
welcome_message = "Welcome to pylings!"
final_message  = "You did it. 🐍"

[[exercises]]
name = "variables1"
path = "exercises/variables/variables1.py"
hint = """
Declare a, b, c with concrete types.
A bare 0 is an int; 0.0 is a float; "" is a str.
"""

[[exercises]]
name = "variables2"
path = "exercises/variables/variables2.py"
hint = "Re-check the value of b so a + b equals 13."
```

### Manifest validation rules

- `format_version` must equal `1`.
- Every `path` must exist relative to the project root.
- Every `name` must be unique.
- The list order *is* the curriculum order. Reorder by editing this file.

---

## Data flow

### Startup

```
launch `pylings`
    │
    ▼
Manifest.load(root)              ← reads info.toml; validates every path exists
    │  (fail → print error w/ line, exit 2)
    ▼
State.load()                     ← reads .pylings/state.json (or creates fresh)
    │
    ▼
For each exercise not yet snapshotted:
    Reset.snapshot(ex)           ← copies pristine source into .pylings/originals/
    │
    ▼
current = State.next_pending(manifest)
    │
    ├── argv "watch" / none → PylingsApp(current).run()
    ├── argv "run X"        → print(Runner.run(X)); exit 0/1
    ├── argv "verify"       → loop all in order; first fail exits 1
    └── …
```

### Watch loop

```
PylingsApp starts
    │
    ▼
Runner.run(current)              ← initial run on launch
    │
    ▼
Render output panel + progress + tree
    │
    ▼
async for _ in Watcher.watch(current.path):     ← debounced 100 ms
    result = Runner.run(current)
    render(result)
    if result.passed and not current.is_pending():
        State.mark_done(current.name)
        play_advance_animation()                ← brief flash + ✓
        current = State.next_pending(manifest)
        if current is None:
            show_final_message(); break
        else:
            switch watcher target → current.path
```

### Pass criteria (both required)

1. `RunResult.exit_code == 0` — no `AssertionError`, no `SyntaxError`, no timeout.
2. `Exercise.is_pending()` returns `False` — the `# I AM NOT DONE` line has been removed.

If exit code is 0 but the marker is still present, the TUI shows: *"Tests pass! Remove the `# I AM NOT DONE` line to advance."* This is the Rustlings nudge that prevents accidental skips.

### Subprocess invocation

```python
subprocess.run(
    [sys.executable, str(ex.path)],
    cwd=root,
    capture_output=True,
    text=True,
    timeout=5.0,
    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
)
```

- `sys.executable` so the exercise runs under the same interpreter pylings was installed into.
- `PYTHONDONTWRITEBYTECODE=1` keeps the exercises tree free of `__pycache__/`.
- 5 s timeout. On `TimeoutExpired`, `RunResult` carries `timed_out=True`.

### State transitions

| Trigger | State change |
|---|---|
| First launch | `state.json` created; all exercises pending |
| Exercise file saved → passes | `completed += {name}`; `current = next pending` |
| `pylings reset X` | `completed -= {X}`; file restored from snapshot; if `X` precedes `current`, `current = X` |
| `pylings verify` | Read-only; never mutates state |
| All exercises pass | `current = None`; final message shown; exit 0 |

---

## Error handling

| Failure mode | Where caught | What the user sees |
|---|---|---|
| `SyntaxError` in exercise | Runner (exit ≠ 0, stderr) | Red panel: traceback w/ Rich syntax highlighting; arrow at the line |
| `AssertionError` in exercise | Runner (exit ≠ 0, stderr) | Red panel: failing line + `assert` expression |
| Exercise hangs / infinite loop | Runner timeout (5 s) | Yellow panel: *"Timed out after 5 s — possible infinite loop? Press `r` to reset."* |
| Exercise prints to stdout & passes | Runner captures stdout | Green panel: stdout above ✓; doesn't block advancement |
| `# I AM NOT DONE` still present, tests pass | `Exercise.is_pending()` after run | Blue nudge: *"Tests pass! Remove `# I AM NOT DONE` to advance."* |
| `info.toml` missing/malformed | `Manifest.load` at startup | Error w/ line number; exit 2; TUI never launches |
| Exercise path in `info.toml` doesn't exist | `Manifest.load` validation | Same as above; names the missing path |
| `.pylings/state.json` corrupted | `State.load` | Warn to stderr; rename to `state.json.bak`; start fresh |
| `originals/<name>` missing on reset | `Reset.restore` | Refuse and print: *"No snapshot for X. Has the file been seen by pylings yet?"* |
| Watchfiles event storm (save loop) | 100 ms debounce in Watcher | At most one rerun per save burst |
| Terminal too small for TUI | Textual dim handling | Compact single-pane fallback (Textual native) |
| `Ctrl+C` mid-run | Signal handler in App + Runner | Subprocess killed; state preserved; clean exit |
| Top-level bug in pylings itself | `try/except` in `cli.main` | Traceback to stderr; exit 1; no recovery attempt |

---

## Testing plan

Three layers, all under the new `tests/` tree (tests of pylings itself, not of exercises):

```
tests/
├── unit/
│   ├── test_manifest.py        ← info.toml parsing, validation errors
│   ├── test_exercise.py        ← done-marker detection edge cases
│   ├── test_runner.py          ← fixture exercises: pass, fail, syntax, hang
│   ├── test_state.py           ← atomic writes, corruption recovery
│   └── test_reset.py           ← snapshot + restore round-trip
├── integration/
│   ├── test_cli_verify.py      ← subprocess.run(["pylings", "verify", ...])
│   ├── test_cli_list.py        ← list output format
│   ├── test_cli_hint.py        ← hint resolution
│   └── test_cli_reset.py       ← reset round-trip via CLI
├── tui/
│   └── test_app_pilot.py       ← Textual Pilot: launch, press h, assert hint visible
└── fixtures/
    └── tiny_curriculum/        ← 3-exercise mini-info.toml for fast tests
        ├── info.toml
        └── exercises/
            ├── passing.py
            ├── asserts.py      ← AssertionError
            └── syntax.py       ← SyntaxError
```

### Fixture strategy

Every runner/CLI test uses `tests/fixtures/tiny_curriculum/`. Tests pass `--root tests/fixtures/tiny_curriculum` to the CLI so the real curriculum never runs during the test suite. This keeps unit tests fast and isolated.

### Coverage targets

- **Runner:** every failure mode in the error-handling matrix has a unit test.
- **Manifest:** each validation error has a dedicated test asserting the error message.
- **State:** write-then-crash recovery is tested by simulating a corrupted file.
- **TUI:** one Pilot smoke test per binding (`h`, `r`, `n`, `q`, `l`). No pixel-diff testing.

### CI

- GitHub Actions matrix: Python 3.11, 3.12, 3.13 on Ubuntu.
- `pylings verify` runs against the real curriculum as the final CI step — guarantees no exercise is broken end-to-end.

---

## Out of scope (deferred)

- Authoring new exercises for the missing topics listed in README (loops, conditionals, lists/tuples, dicts, file I/O, exceptions, OOP). Will be addressed in a separate curriculum-expansion plan.
- Windows CI matrix entry. Will be added after Linux/macOS support is solid.
- Multiple concurrent students / cloud sync of state. Pylings is single-user local.
- i18n. Hints and messages are English-only.

---

## Success criteria

The redesign is considered done when:

1. A new user runs `pipx install pylings` (or `pip install -e .` from a clone), invokes `pylings`, sees a friendly TUI, and works through the curriculum without ever leaving the terminal.
2. Editing a current exercise file triggers an automatic rerun within 200 ms of save.
3. Removing `# I AM NOT DONE` from a passing exercise advances the learner to the next one with a visible transition.
4. `pylings hint`, `pylings list`, `pylings reset`, `pylings verify` all behave as specified.
5. CI runs `pylings verify` green on the real curriculum across Python 3.11/3.12/3.13.
6. The unit + integration + TUI test suites for pylings itself pass.
