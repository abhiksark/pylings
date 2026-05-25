# Pylings Interaction Model Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade pylings interactions so first launch, resume, topic navigation, output guidance, hints, and instant advancement feel intuitive for beginners.

**Architecture:** Keep the existing Textual app shape. Extend state with optional resume/orientation fields, route startup in `PylingsApp`, improve `TopicPickerScreen` and `TrackScreen`, and make `OutputPanel` a guided status panel while leaving runner/check semantics unchanged.

**Tech Stack:** Python 3.11, Textual, argparse, pytest, pytest-asyncio.

---

## File Structure

- Modify `pylings/core/state.py`: add `seen_intro`, `last_topic`, and `last_exercise` fields plus persistence.
- Modify `pylings/cli.py`: add `topics` subcommand and pass a picker override to the app.
- Modify `pylings/app.py`: choose picker vs resume route on startup.
- Modify `pylings/screens/topic_picker.py`: add Smart Picker banner, row labels, initial selection, and state updates.
- Modify `pylings/screens/track.py`: persist resume target, show running state, track failures, reset hint state, and keep `F4`/quit flush behavior correct.
- Modify `pylings/widgets/output_panel.py`: render Guided Panel states, goal text, details, and progressive hints.
- Modify `pylings/pylings.tcss`: style picker banner and guided panel sections.
- Modify `tests/unit/test_state.py`: cover optional UX fields and backward-compatible v2 state.
- Modify `tests/integration/test_cli_topics.py`: cover parser support for `topics`.
- Modify `tests/tui/test_app_pilot.py`: cover startup routing, picker labels, resume, invalid resume fallback, `F4`, and instant advance.
- Add `tests/tui/test_output_panel.py`: cover guided panel rendering and progressive hints.

---

### Task 1: State Model

**Files:**
- Modify: `pylings/core/state.py`
- Modify: `tests/unit/test_state.py`

- [ ] **Step 1: Write failing state tests**

Add these tests to `tests/unit/test_state.py`:

```python
def test_save_then_load_ux_fields(tmp_path: Path) -> None:
    save(
        tmp_path,
        State(
            completed={"a"},
            seen_intro=True,
            last_topic="alpha",
            last_exercise="a2",
        ),
    )
    loaded = load(tmp_path)
    assert loaded.completed == {"a"}
    assert loaded.seen_intro is True
    assert loaded.last_topic == "alpha"
    assert loaded.last_exercise == "a2"


def test_missing_ux_fields_default_for_existing_v2_state(tmp_path: Path) -> None:
    import json

    pdir = tmp_path / ".pylings"
    pdir.mkdir()
    (pdir / "state.json").write_text(
        json.dumps({"format_version": 2, "completed": ["x"]}),
        encoding="utf-8",
    )
    loaded = load(tmp_path)
    assert loaded.completed == {"x"}
    assert loaded.seen_intro is False
    assert loaded.last_topic is None
    assert loaded.last_exercise is None


def test_record_resume_marks_intro_seen() -> None:
    state = State()
    state.record_resume("alpha", "a1")
    assert state.seen_intro is True
    assert state.last_topic == "alpha"
    assert state.last_exercise == "a1"


def test_clear_resume_keeps_intro_seen() -> None:
    state = State(seen_intro=True, last_topic="alpha", last_exercise="a1")
    state.clear_resume()
    assert state.seen_intro is True
    assert state.last_topic is None
    assert state.last_exercise is None
```

- [ ] **Step 2: Run state tests and confirm failure**

Run: `pytest tests/unit/test_state.py -q`

Expected: FAIL because `State` does not accept UX fields and has no `record_resume` or `clear_resume`.

- [ ] **Step 3: Implement state fields and helpers**

Change `State` and load/save behavior in `pylings/core/state.py` to:

```python
@dataclass
class State:
    completed: set[str] = field(default_factory=set)
    seen_intro: bool = False
    last_topic: str | None = None
    last_exercise: str | None = None

    def mark_done(self, name: str) -> None:
        self.completed.add(name)

    def record_resume(self, topic: str, exercise: str | None) -> None:
        self.seen_intro = True
        self.last_topic = topic
        self.last_exercise = exercise

    def clear_resume(self) -> None:
        self.last_topic = None
        self.last_exercise = None
```

Load optional fields with defaults:

```python
return State(
    completed=set(data.get("completed", [])),
    seen_intro=bool(data.get("seen_intro", False)),
    last_topic=data.get("last_topic"),
    last_exercise=data.get("last_exercise"),
)
```

Save them atomically:

```python
payload = {
    "format_version": FORMAT_VERSION,
    "completed": sorted(state.completed),
    "seen_intro": state.seen_intro,
    "last_topic": state.last_topic,
    "last_exercise": state.last_exercise,
}
```

- [ ] **Step 4: Run state tests and confirm pass**

Run: `pytest tests/unit/test_state.py -q`

Expected: PASS.

- [ ] **Step 5: Commit**

Run:

```bash
git add pylings/core/state.py tests/unit/test_state.py
git commit -m "feat: persist interaction resume state"
```

---

### Task 2: Launch Routing And CLI

**Files:**
- Modify: `pylings/app.py`
- Modify: `pylings/cli.py`
- Modify: `tests/tui/test_app_pilot.py`
- Modify: `tests/integration/test_cli_topics.py`

- [ ] **Step 1: Write failing launch and parser tests**

Add to `tests/tui/test_app_pilot.py`:

```python
from pylings.core.state import State, save as save_state


@pytest.mark.asyncio
async def test_default_launch_resumes_last_incomplete_exercise(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    save_state(work, State(seen_intro=True, last_topic="alpha", last_exercise="a2"))
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TrackScreen)
        assert app.screen.topic == "alpha"
        assert app.screen.current == "a2"


@pytest.mark.asyncio
async def test_default_launch_ignores_invalid_resume_state(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    save_state(work, State(seen_intro=True, last_topic="missing", last_exercise="ghost"))
    app = PylingsApp(root=work)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TopicPickerScreen)


@pytest.mark.asyncio
async def test_force_picker_launch_ignores_resume_state(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    save_state(work, State(seen_intro=True, last_topic="alpha", last_exercise="a2"))
    app = PylingsApp(root=work, force_picker=True)
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert isinstance(app.screen, TopicPickerScreen)
```

Add to `tests/integration/test_cli_topics.py`:

```python
from pylings.cli import _build_parser


def test_topics_subcommand_parses() -> None:
    args = _build_parser().parse_args(["topics"])
    assert args.command == "topics"
```

- [ ] **Step 2: Run targeted tests and confirm failure**

Run: `pytest tests/tui/test_app_pilot.py::test_default_launch_resumes_last_incomplete_exercise tests/tui/test_app_pilot.py::test_default_launch_ignores_invalid_resume_state tests/tui/test_app_pilot.py::test_force_picker_launch_ignores_resume_state tests/integration/test_cli_topics.py::test_topics_subcommand_parses -q`

Expected: FAIL because `force_picker`, resume routing, and `topics` parser support do not exist.

- [ ] **Step 3: Implement app startup routing**

Change `PylingsApp.__init__` in `pylings/app.py`:

```python
def __init__(
    self,
    root: Path,
    start_topic: str | None = None,
    force_picker: bool = False,
) -> None:
    super().__init__()
    self.root = root
    self.manifest: Manifest = load_manifest(root)
    self.state: State = load_state(root)
    self._start_topic = start_topic
    self._force_picker = force_picker
```

Add helpers:

```python
def _topic_is_open(self, topic: str | None) -> bool:
    return topic in self.manifest.topics() if topic is not None else False

def _resume_topic(self) -> str | None:
    if not self.state.seen_intro or self._force_picker:
        return None
    topic = self.state.last_topic
    if not self._topic_is_open(topic):
        return None
    assert topic is not None
    if any(ex.name not in self.state.completed for ex in self.manifest.exercises_in(topic)):
        return topic
    return None
```

Change `on_mount`:

```python
def on_mount(self) -> None:
    self.push_screen(TopicPickerScreen())
    topic = self._start_topic if self._start_topic is not None else self._resume_topic()
    if topic is not None and topic in self.manifest.topics():
        self.push_screen(TrackScreen(topic))
```

Change `run_tui`:

```python
def run_tui(root: Path, start_topic: str | None = None, force_picker: bool = False) -> int:
    return PylingsApp(root, start_topic, force_picker=force_picker).run() or 0
```

- [ ] **Step 4: Implement `topics` CLI command**

In `pylings/cli.py`, add parser:

```python
sub.add_parser("topics", help="Launch the TUI on the topic picker.")
```

Update dispatch:

```python
if args.command in (None, "watch", "start", "topics"):
    start_topic = getattr(args, "topic", None)
    if start_topic is not None:
        from pylings.core.manifest import load as load_manifest
        if _resolve_topic(load_manifest(args.root), start_topic) is None:
            return 2
    from pylings.app import run_tui
    return run_tui(args.root, start_topic, force_picker=args.command == "topics")
```

- [ ] **Step 5: Run targeted tests and confirm pass**

Run: `pytest tests/tui/test_app_pilot.py tests/integration/test_cli_topics.py -q`

Expected: PASS.

- [ ] **Step 6: Commit**

Run:

```bash
git add pylings/app.py pylings/cli.py tests/tui/test_app_pilot.py tests/integration/test_cli_topics.py
git commit -m "feat: resume or open topics on launch"
```

---

### Task 3: Smart Picker

**Files:**
- Modify: `pylings/screens/topic_picker.py`
- Modify: `pylings/pylings.tcss`
- Modify: `tests/tui/test_app_pilot.py`

- [ ] **Step 1: Write failing picker tests**

Add to `tests/tui/test_app_pilot.py`:

```python
@pytest.mark.asyncio
async def test_picker_shows_first_run_start_banner(tmp_path: Path) -> None:
    app = PylingsApp(root=_work_copy(tmp_path), force_picker=True)
    async with app.run_test() as pilot:
        await _settle(pilot)
        banner = str(app.screen.query_one("#topic-banner").renderable)
        assert "Start here" in banner
        assert "alpha" in banner


@pytest.mark.asyncio
async def test_picker_rows_show_status_labels(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    save_state(work, State(completed={"a1"}, seen_intro=True, last_topic="alpha"))
    app = PylingsApp(root=work, force_picker=True)
    async with app.run_test() as pilot:
        await _settle(pilot)
        rendered = " ".join(str(row.content) for row in app.screen.query(".topic-row").results())
        assert "Continue" in rendered
        assert "Start" in rendered
```

- [ ] **Step 2: Run picker tests and confirm failure**

Run: `pytest tests/tui/test_app_pilot.py::test_picker_shows_first_run_start_banner tests/tui/test_app_pilot.py::test_picker_rows_show_status_labels -q`

Expected: FAIL because `#topic-banner` and row labels do not exist.

- [ ] **Step 3: Implement Smart Picker render**

In `pylings/screens/topic_picker.py`, compose a banner before the list:

```python
yield Static("", id="topic-banner")
yield VerticalScroll(ListView(id="topics"))
```

Add helper methods:

```python
def _topic_progress(self, topic: str) -> tuple[int, int]:
    exs = self.app.manifest.exercises_in(topic)
    done = sum(1 for ex in exs if ex.name in self.app.state.completed)
    return done, len(exs)

def _first_incomplete_topic(self) -> str | None:
    for topic in self.app.manifest.topics():
        done, total = self._topic_progress(topic)
        if done < total:
            return topic
    return None

def _banner_text(self) -> str:
    first = self._first_incomplete_topic()
    if first is None:
        return self.app.manifest.final_message
    if not self.app.state.seen_intro:
        return f"Start here: {first}"
    if self.app.state.last_topic is None:
        return "Choose a topic to practice."
    return "Topics"
```

Update `_populate` to set the banner and row labels:

```python
self.query_one("#topic-banner", Static).update(self._banner_text())
for topic in manifest.topics():
    exs = manifest.exercises_in(topic)
    done = sum(1 for ex in exs if ex.name in completed)
    if done == len(exs):
        mark = "✓"
        label_text = "Done"
    elif done:
        mark = "●"
        label_text = "Continue"
    else:
        mark = " "
        label_text = "Start"
    label = f"{mark}  {topic:<18} {done}/{len(exs):<5} {label_text}"
    listview.append(ListItem(Static(label, classes="topic-row"), name=topic))
```

When a topic is selected, mark intro seen and persist:

```python
self.app.state.record_resume(topic, None)
save_state(self.app.root, self.app.state)
self.app.push_screen(TrackScreen(topic))
```

Import `save_state`.

- [ ] **Step 4: Add picker CSS**

Add to `pylings/pylings.tcss`:

```css
#topic-banner {
    height: auto;
    padding: 1 2;
    background: $primary 20%;
    color: $text;
    border-bottom: solid $primary;
}
```

- [ ] **Step 5: Run picker tests and confirm pass**

Run: `pytest tests/tui/test_app_pilot.py -q`

Expected: PASS.

- [ ] **Step 6: Commit**

Run:

```bash
git add pylings/screens/topic_picker.py pylings/pylings.tcss tests/tui/test_app_pilot.py
git commit -m "feat: make topic picker state aware"
```

---

### Task 4: Guided Panel And Progressive Hints

**Files:**
- Modify: `pylings/widgets/output_panel.py`
- Modify: `pylings/pylings.tcss`
- Add: `tests/tui/test_output_panel.py`

- [ ] **Step 1: Write failing output panel tests**

Create `tests/tui/test_output_panel.py`:

```python
from pathlib import Path

import pytest
from textual.app import App, ComposeResult
from textual.widgets import Static

from pylings.core.exercise import Exercise, RunResult
from pylings.widgets.output_panel import OutputPanel


class _Harness(App[None]):
    def compose(self) -> ComposeResult:
        yield OutputPanel()


def _exercise(tmp_path: Path, text: str, hint: str = "Use a string. Then remove the marker.") -> Exercise:
    path = tmp_path / "variables1.py"
    path.write_text(text, encoding="utf-8")
    return Exercise(
        name="variables1",
        path=path,
        check_path=tmp_path / "check.py",
        topic="variables",
        hint=hint,
    )


def _result(exit_code: int, stdout: str = "", stderr: str = "", timed_out: bool = False) -> RunResult:
    return RunResult(
        passed=exit_code == 0 and not timed_out,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
        duration_s=0.1,
        timed_out=timed_out,
    )


@pytest.mark.asyncio
async def test_render_running_state(tmp_path: Path) -> None:
    app = _Harness()
    async with app.run_test() as pilot:
        await pilot.pause()
        panel = app.query_one(OutputPanel)
        panel.render_running(_exercise(tmp_path, "# Goal: set name\nname = broken\n"), 0, 2)
        await pilot.pause()
        assert "Running checks" in str(panel.query_one("#status", Static).renderable)


@pytest.mark.asyncio
async def test_failure_shows_goal_status_next_step_and_details(tmp_path: Path) -> None:
    app = _Harness()
    async with app.run_test() as pilot:
        await pilot.pause()
        panel = app.query_one(OutputPanel)
        ex = _exercise(tmp_path, "# Goal: set name\nname = broken\n")
        panel.render_result(ex, _result(1, stderr="NameError: broken"), failures=1, completed=0, total=2)
        await pilot.pause()
        rendered = panel.renderable_text()
        assert "Goal" in rendered
        assert "set name" in rendered
        assert "Not passing yet" in rendered
        assert "NameError: broken" in rendered
        assert "Use a string." in rendered


@pytest.mark.asyncio
async def test_marker_pass_prompts_marker_removal(tmp_path: Path) -> None:
    app = _Harness()
    async with app.run_test() as pilot:
        await pilot.pause()
        panel = app.query_one(OutputPanel)
        ex = _exercise(tmp_path, "# I AM NOT DONE\nvalue = 1\n")
        panel.render_result(ex, _result(0, stdout="ok"), failures=0, completed=0, total=2)
        await pilot.pause()
        assert "remove marker" in panel.renderable_text().lower()


@pytest.mark.asyncio
async def test_full_hint_toggles_on_f1(tmp_path: Path) -> None:
    app = _Harness()
    async with app.run_test() as pilot:
        await pilot.pause()
        panel = app.query_one(OutputPanel)
        panel.toggle_hint("Full hint text.")
        await pilot.pause()
        assert "Full hint text." in str(panel.query_one("#hint", Static).renderable)
```

- [ ] **Step 2: Run output panel tests and confirm failure**

Run: `pytest tests/tui/test_output_panel.py -q`

Expected: FAIL because guided panel IDs, `render_running`, `renderable_text`, and new `render_result` parameters do not exist.

- [ ] **Step 3: Implement Guided Panel widget**

Update `OutputPanel.compose`:

```python
yield Static("", id="output-header")
yield Static("", id="goal")
yield Static("", id="status")
yield Static("", id="next-step")
yield Static("", id="details")
yield Static("", id="hint")
```

Add helpers:

```python
def renderable_text(self) -> str:
    parts = []
    for widget_id in ("output-header", "goal", "status", "next-step", "details", "hint"):
        widget = self.query_one(f"#{widget_id}", Static)
        parts.append(str(widget.renderable))
    return "\n".join(parts)

def _goal_from(self, exercise: Exercise) -> str:
    for line in exercise.path.read_text(encoding="utf-8").splitlines()[:12]:
        stripped = line.strip()
        if stripped.startswith("# Goal:"):
            return stripped.removeprefix("# Goal:").strip()
        if stripped.startswith("# Exercise:"):
            return stripped.removeprefix("# Exercise:").strip()
    return exercise.name

def _hint_nudge(self, exercise: Exercise) -> str:
    first = exercise.hint.strip().split(".")[0].strip()
    return f"{first}." if first else "Hint available: press F1."
```

Implement `render_running`:

```python
def render_running(self, exercise: Exercise, completed: int = 0, total: int = 0) -> None:
    self.remove_class("passed", "failed", "pending")
    self.query_one("#output-header", Static).update(
        f"[bold]{exercise.name}[/bold]   [dim]{self._display_path(exercise)}[/dim]"
    )
    self.query_one("#goal", Static).update(f"[bold]Goal[/bold]\n{self._goal_from(exercise)}")
    self.query_one("#status", Static).update("[bold blue]Running checks...[/bold blue]")
    self.query_one("#next-step", Static).update("Keep editing; results update automatically.")
    self.query_one("#details", Static).update("")
```

Update `render_result` signature:

```python
def render_result(
    self,
    exercise: Exercise,
    result: RunResult,
    failures: int = 0,
    completed: int = 0,
    total: int = 0,
) -> None:
```

Inside `render_result`, update the sections rather than one body block:

```python
self._render_header(exercise, completed, total)
self.query_one("#goal", Static).update(f"[bold]Goal[/bold]\n{self._goal_from(exercise)}")
details = (result.stderr or result.stdout).rstrip()
self.query_one("#details", Static).update(f"[bold]Details[/bold]\n{details}" if details else "")
```

Use status/next-step text for timeout, non-zero, marker pass, and complete:

```python
if result.timed_out:
    self.add_class("failed")
    self.query_one("#status", Static).update("[bold red]Not passing yet[/bold red]")
    self.query_one("#next-step", Static).update("This timed out. Check for an infinite loop.")
elif result.exit_code != 0:
    self.add_class("failed")
    self.query_one("#status", Static).update("[bold red]Not passing yet[/bold red]")
    nudge = self._hint_nudge(exercise) if failures else "Hint available: press F1."
    self.query_one("#next-step", Static).update(f"Read the details, fix the code, then pause typing.\n{nudge}")
elif exercise.is_pending():
    self.add_class("pending")
    self.query_one("#status", Static).update("[bold yellow]Checks pass, remove marker[/bold yellow]")
    self.query_one("#next-step", Static).update("Remove the # I AM NOT DONE line to advance.")
else:
    self.add_class("passed")
    self.query_one("#status", Static).update(f"[bold green]✓ {exercise.name} complete[/bold green]")
    self.query_one("#next-step", Static).update("Loading the next exercise.")
```

Change `_render_header` to include progress:

```python
def _render_header(self, exercise: Exercise, completed: int = 0, total: int = 0) -> None:
    progress = f"   [dim]{completed}/{total} complete[/dim]" if total else ""
    self.query_one("#output-header", Static).update(
        f"[bold]{exercise.name}[/bold]{progress}   [dim]{self._display_path(exercise)}[/dim]"
    )
```

- [ ] **Step 4: Add guided panel CSS**

Add to `pylings/pylings.tcss`:

```css
#goal,
#status,
#next-step,
#details {
    padding: 1 0 0 0;
}
```

- [ ] **Step 5: Run output panel tests and confirm pass**

Run: `pytest tests/tui/test_output_panel.py -q`

Expected: PASS.

- [ ] **Step 6: Commit**

Run:

```bash
git add pylings/widgets/output_panel.py pylings/pylings.tcss tests/tui/test_output_panel.py
git commit -m "feat: guide learners through check output"
```

---

### Task 5: Track Integration And Full Verification

**Files:**
- Modify: `pylings/screens/track.py`
- Modify: `tests/tui/test_app_pilot.py`
- Modify: `Readme.md`

- [ ] **Step 1: Write failing track integration tests**

Add to `tests/tui/test_app_pilot.py`:

```python
@pytest.mark.asyncio
async def test_track_records_resume_when_loaded(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PylingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        assert app.state.seen_intro is True
        assert app.state.last_topic == "alpha"
        assert app.state.last_exercise == "a1"


@pytest.mark.asyncio
async def test_instant_advance_updates_resume_to_next_exercise(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PylingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        track.query_one("#code", TextArea).text = "x = 1\n"
        track._flush_and_run()
        await _settle(pilot)
        assert "a1" in app.state.completed
        assert track.current == "a2"
        assert app.state.last_topic == "alpha"
        assert app.state.last_exercise == "a2"


@pytest.mark.asyncio
async def test_failed_run_shows_progressive_nudge(tmp_path: Path) -> None:
    work = _work_copy(tmp_path)
    app = PylingsApp(root=work, start_topic="alpha")
    async with app.run_test() as pilot:
        await _settle(pilot)
        track = app.screen
        assert isinstance(track, TrackScreen)
        track.query_one("#code", TextArea).text = "x = 99\n"
        track._flush_and_run()
        await _settle(pilot)
        assert "alpha one" in track.query_one(OutputPanel).renderable_text()
```

- [ ] **Step 2: Run integration tests and confirm failure**

Run: `pytest tests/tui/test_app_pilot.py -q`

Expected: FAIL because track does not persist resume state, pass progress to output, show running state, or track failure counts.

- [ ] **Step 3: Implement track integration**

In `TrackScreen.__init__`, add:

```python
self._failure_counts: dict[str, int] = {}
```

In `_render_state`, leave progress/tree updates as-is.

Add progress helper:

```python
def _progress_counts(self) -> tuple[int, int]:
    exs = self._exercises()
    done = sum(1 for ex in exs if ex.name in self.app.state.completed)
    return done, len(exs)
```

Update `_load_current` after loading editor:

```python
self._failure_counts[self.current] = 0
self.app.state.record_resume(self.topic, self.current)
save_state(self.app.root, self.app.state)
```

Update `_run_current` before starting the worker:

```python
completed, total = self._progress_counts()
self.query_one(OutputPanel).render_running(ex, completed, total)
```

Update `_apply_result` before rendering:

```python
if not result.passed:
    self._failure_counts[exercise.name] = self._failure_counts.get(exercise.name, 0) + 1
else:
    self._failure_counts[exercise.name] = 0
completed, total = self._progress_counts()
self.query_one(OutputPanel).render_result(
    exercise,
    result,
    failures=self._failure_counts.get(exercise.name, 0),
    completed=completed,
    total=total,
)
```

When topic completes:

```python
self.app.state.record_resume(self.topic, None)
save_state(self.app.root, self.app.state)
```

When `action_topics` runs, ensure `seen_intro` is true and save:

```python
if self.current is not None:
    self.app.state.record_resume(self.topic, self.current)
save_state(self.app.root, self.app.state)
self.app.pop_screen()
```

- [ ] **Step 4: Update README command docs**

In `Readme.md`, add:

```bash
pylings topics                         # opens the topic picker
```

Update TUI text to mention first-run picker and returning resume behavior.

- [ ] **Step 5: Run targeted tests**

Run: `pytest tests/unit/test_state.py tests/integration/test_cli_topics.py tests/tui/test_output_panel.py tests/tui/test_app_pilot.py -q`

Expected: PASS.

- [ ] **Step 6: Run full suite**

Run: `pytest -q`

Expected: PASS.

- [ ] **Step 7: Commit**

Run:

```bash
git add Readme.md pylings/screens/track.py tests/tui/test_app_pilot.py
git commit -m "feat: integrate intuitive solve loop"
```
