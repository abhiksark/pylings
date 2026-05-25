# Pylings — Built-in Editor Design

**Date:** 2026-05-20
**Status:** Design approved, pending implementation plan
**Owner:** abhiksark@gmail.com
**Supersedes (in part):** the editing-workflow assumptions in `2026-05-19-pylings-rustlings-ux-design.md`

## Goal

Make pylings genuinely beginner-proof to *edit in*. Today, running `pylings` shows the exercise and its checks, but the learner must open the file in their own editor. The short-lived `e`-key feature tried to launch `$EDITOR`, which assumed the learner has an editor configured and knows how to drive it — a bad assumption for absolute beginners (the classic "dropped into vim, can't get out").

This design replaces external editing with a **built-in editor pane** inside the TUI. The learner types their fix directly in pylings; checks re-run automatically. No external editor, no `$EDITOR`, no assumptions.

## Why this matters

A learner reported running `pylings` and "not understanding it" — and was rightly wary that beginners won't know vim. A Rustlings-style tool for *Python beginners* should not require the learner to already have a working editor setup. Owning the editing surface removes the single biggest setup hurdle.

## Non-goals

- Replacing core modules. `manifest`, `runner`, `state`, `reset`, `exercise` are untouched.
- Changing the CLI. `verify` / `list` / `hint` / `run` / `reset` are unchanged. `pylings` and `pylings watch` still launch the TUI.
- Supporting simultaneous external-editor editing. The built-in editor is the sole editing surface (see Decisions).
- A full IDE. No linting, completion, or multi-file editing — just the current exercise.

---

## Decisions locked in during brainstorming

| Topic | Decision |
|---|---|
| Editing surface | Built-in editor pane inside the TUI (Textual `TextArea`) |
| Layout | Editor and Output side by side; exercise tree hidden, toggled on demand |
| Save model | Auto-save — debounced write + re-run as you type; no save key |
| External editing | Not supported; the file watcher is removed entirely |
| Syntax highlighting | Yes — `textual[syntax]` (tree-sitter Python grammar) |
| Run execution | On a Textual thread worker, so the editor stays smooth |

---

## Architecture

This is a TUI-layer change. Core (`pylings/core/*` except `watcher.py`) and the CLI are untouched.

### File changes

```
pylings/
├── pyproject.toml                ← MODIFY: drop watchfiles, textual → textual[syntax]
├── Readme.md                     ← MODIFY: key table + workflow
├── pylings/
│   ├── app.py                    ← MODIFY: layout, auto-save worker, removals
│   ├── pylings.tcss              ← MODIFY: editor|output layout, tree toggle
│   ├── widgets/
│   │   ├── editor_pane.py        ← NEW: EditorPane (wraps TextArea)
│   │   ├── output_panel.py       ← MODIFY: header text reworded
│   │   ├── exercise_tree.py      ← unchanged
│   │   └── progress.py           ← unchanged
│   └── core/
│       └── watcher.py            ← DELETE
└── tests/
    ├── unit/test_watcher.py      ← DELETE
    └── tui/test_app_pilot.py     ← MODIFY: retarget bindings, add editor tests
```

### Dependencies

- **Drop** `watchfiles` — only the watcher used it.
- **Change** `textual` → `textual[syntax]` — the `syntax` extra pulls the `tree-sitter` Python grammar that `TextArea` needs for highlighting. Without it, `TextArea` silently falls back to monochrome (so a missing grammar degrades gracefully, but the dependency makes highlighting the default).
- Pin to the tested major: `textual[syntax]>=8.0.0`.

---

## The keybinding problem

Once the `TextArea` has focus and the learner is typing, **single-letter app bindings collide with typing** — pressing `h` to type the letter "h" would otherwise fire the hint action. So the previous letter bindings (`h`/`r`/`l`/`n`/`q`) cannot survive an in-pane editor.

**Resolution — every action uses a non-typing key:**

| Key | Action |
|---|---|
| `F1` | Toggle hint |
| `F2` | Reset current exercise |
| `F3` | Toggle exercise list (tree) |
| `Ctrl+Q` | Quit |

- Function keys and `Ctrl+Q` are never consumed by `TextArea`, so they work whether or not the editor is focused — no focus-mode switching.
- The check needs **no key** — auto-save runs it.
- `n` (skip-animation) is **dropped**; it was a no-op placeholder for an unimplemented animation.
- Textual's `Footer` renders all four, keeping them discoverable.

---

## Components

### `EditorPane` (`pylings/widgets/editor_pane.py`) — NEW

A thin wrapper over Textual's `TextArea`.

```python
class EditorPane(Vertical):
    def compose(self) -> ComposeResult:
        yield TextArea.code_editor("", language="python", id="code")

    def load_exercise(self, exercise: Exercise) -> None:
        """Read the exercise file from disk into the editor."""
        area = self.query_one("#code", TextArea)
        area.text = exercise.path.read_text(encoding="utf-8")
        area.move_cursor((0, 0))

    @property
    def text(self) -> str:
        return self.query_one("#code", TextArea).text
```

`TextArea.code_editor(...)` gives multi-line editing, Python syntax highlighting, 4-space soft tabs, undo/redo, and selection out of the box.

### `app.py` — MODIFIED

Owns the debounce timer and the run worker; wires the editor to the auto-save loop.

```python
def compose(self) -> ComposeResult:
    yield Header()
    yield ProgressBar(id="progress")
    yield Horizontal(
        ExerciseTree(),            # #tree, display:none by default
        EditorPane(id="editor"),
        OutputPanel(id="output"),
        id="main",
    )
    yield Footer()
```

Bindings become:

```python
BINDINGS = [
    Binding("f1", "toggle_hint", "Hint"),
    Binding("f2", "reset", "Reset"),
    Binding("f3", "toggle_list", "List"),
    Binding("ctrl+q", "quit", "Quit"),
]
```

### `OutputPanel` — MODIFIED

Header text reworded. It currently reads "Press e to open this file…". New header:

- Line 1: exercise name (bold) + file path (dim, for reference).
- Line 2: *"Edit the code on the left. Checks update automatically as you type."*

The pass/fail/pending body and the hint section are unchanged.

---

## Data flow

### Startup

```
launch `pylings`
    │
    ▼
Manifest.load / State.load            (unchanged)
    │
    ▼
PylingsApp.on_mount():
    EditorPane.load_exercise(current)
    focus the TextArea
    run current once → OutputPanel.render_result(...)
    render ProgressBar + ExerciseTree
```

### The auto-save → run loop

```
learner types in the TextArea
        │
        ▼
TextArea.Changed  ──►  App.on_text_area_changed()
        │
        ▼
restart 600 ms debounce timer   (each keystroke cancels + restarts it)
        │  timer fires (typing paused)
        ▼
_flush_and_run():
    write EditorPane.text → current exercise file        (auto-save)
    start run worker  (@work thread=True, exclusive=True)
        │
        ▼  (worker thread)
    runner.run(current) → RunResult
        │  call_from_thread
        ▼  (main thread)
_apply_result(exercise, result):
    OutputPanel.render_result(exercise, result)
    if result.passed:
        state.mark_done(exercise.name, manifest)
        save_state(root, state)
        advance: cancel timer, EditorPane.load_exercise(next)
        re-render ProgressBar + ExerciseTree
        run the new current exercise once
    if current is None (curriculum complete):
        show final message, exit 0
```

### Pass criteria

Unchanged from the original design — `RunResult.passed` is `exit_code == 0 AND not timed_out AND not exercise.is_pending()`. The learner deletes the `# I AM NOT DONE` line *in the editor*; auto-save writes it out; the next run sees the marker gone.

### Worker semantics

- `@work(thread=True, exclusive=True)` — the run executes off the event loop, so the editor never stutters. `exclusive=True` means a new flush cancels a still-running stale run; no subprocess backlog.

### Reset (`F2`)

```
F2 → action_reset():
    cancel pending debounce timer
    reset.restore(root, current)          (file ← snapshot)
    EditorPane.load_exercise(current)     (editor ← restored file)
    run current once → render
```

State semantics are unchanged: resetting the *current* exercise does not move the cursor or alter `completed`.

### Quit (`Ctrl+Q`)

`action_quit()` cancels the pending debounce timer but first writes `EditorPane.text` to disk, so the last <600 ms of typing is not lost, then exits.

### Implementation note — programmatic loads vs. user typing

Setting `TextArea.text` in `load_exercise()` itself emits a `TextArea.Changed` message — so loading an exercise (on mount, on advance, on reset) would otherwise restart the debounce timer and trigger a spurious auto-save + run of the freshly-loaded, unmodified file.

The App must distinguish a programmatic load from real typing. The plan should set a short-lived "loading" flag around `load_exercise()` and have `on_text_area_changed` ignore `Changed` messages while it is set. Each load path (`on_mount`, advance, reset) then runs the exercise *once*, explicitly — not via the debounce.

---

## Error handling

| Situation | Behavior |
|---|---|
| Mid-edit `SyntaxError` (incomplete code) | Debounce limits runs to typing pauses; OutputPanel shows "Not passing yet" + the error. Expected, not alarming. |
| Exercise file unreadable on `load_exercise` | Surface the error in the OutputPanel; do not crash the app. |
| Run worker raises unexpectedly | Caught at the worker boundary; rendered as a failure in the OutputPanel. |
| Terminal too small | Textual's native compact reflow (unchanged). |
| `tree-sitter` Python grammar missing | `TextArea` falls back to plain monochrome text; editing still fully works. |
| Curriculum complete (no next exercise) | Final message shown, app exits 0. |

---

## Testing

All tests live under `tests/` (tests of pylings itself).

### Deleted

- `tests/unit/test_watcher.py` — module removed.
- From `tests/tui/test_app_pilot.py`: the `e`-binding smoke test and the three `_resolve_editor` unit tests.

### Updated — `tests/tui/test_app_pilot.py`

Binding tests retarget to the new keys:

- hint toggle: `h` → `F1`
- reset: `r` → `F2`
- list toggle: `l` → `F3`
- quit: `q` → `Ctrl+Q`

### New — `tests/tui/test_app_pilot.py` (Textual `Pilot`)

1. **Editor loads the exercise** — on mount, the `TextArea` text equals the current exercise file's content.
2. **Typing auto-saves and re-runs** — set the `TextArea` text to broken code, `await pilot.pause(~0.8s)` for the debounce, assert the file on disk matches the new text and the OutputPanel shows a failure.
3. **Solving advances** — set the `TextArea` to a known-good solution with the `# I AM NOT DONE` line removed, wait for the debounce, assert the exercise is marked complete and the editor has loaded the next exercise.
4. **`F2` reset reloads the editor** — scribble in the editor, wait for auto-save, press `F2`, assert the `TextArea` text is back to pristine snapshot content.

### Fixtures

Pilot tests copy `tests/fixtures/tiny_curriculum` into `tmp_path` (established pattern). The "solving advances" test rewrites a fixture exercise to a known-good solution so it is deterministic regardless of the fixture's starting content.

### Unaffected

Every `tests/unit/` core test (manifest, runner, state, reset, exercise) and every `tests/integration/` CLI test, including the cold-start guard — the CLI and core are untouched.

### Rough count

67 tests today → remove ~6 → add ~5 → ~66, all green.

---

## Out of scope (deferred)

- Locking the `# --- checks (do not edit below) ---` block so the learner can't edit the asserts. Rustlings allows editing anything; same here. The comment is the only guard.
- An in-editor "you've completed everything" celebration animation. `n` and `action_skip_animation` are removed; if an animation is added later it gets its own design.
- Re-introducing external-editor support. If demanded later, it returns as its own spec (watcher + reload-on-clean + own-write suppression).

---

## Success criteria

1. `pylings` launches; the learner sees the exercise code in an editable pane and can immediately type — no external editor, no `$EDITOR`.
2. Pausing after typing auto-saves the file and re-runs the check; the OutputPanel updates within ~1 s.
3. Writing a correct solution and removing `# I AM NOT DONE` advances to the next exercise, which loads into the editor.
4. `F1`/`F2`/`F3`/`Ctrl+Q` all work while the editor is focused.
5. Syntax highlighting is visible for Python code in the editor.
6. The `watchfiles` dependency is gone; `textual[syntax]` is in.
7. The full test suite is green.
