# Pylings Product Maturity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Pylings a self-contained installable learning product instead of a repo-bound TUI.

**Architecture:** Keep the existing Textual app and manifest model, but add a packaged curriculum layer that can initialize and update learner workspaces. Reset, run, verify, and future solution commands should operate against explicit workspace roots while pristine exercise/check data comes from packaged resources.

**Tech Stack:** Python 3.11+, Textual, argparse, hatchling, importlib.resources, pathlib/shutil, subprocess, pytest, GitHub Actions.

---

## File Structure

- Create `pylings/core/curriculum.py`: packaged curriculum discovery, resource copying, workspace init/update helpers.
- Modify `pylings/core/exercise.py`: add optional `root`, `rel_path`, and `check_rel_path` metadata needed by reset and runner.
- Modify `pylings/core/manifest.py`: populate exercise metadata from `info.toml`.
- Modify `pylings/core/reset.py`: restore from `.pylings/originals/` created from pristine curriculum, not from first-seen edited files.
- Modify `pylings/core/runner.py`: run compiled exercise/check code with real filenames and workspace cwd.
- Modify `pylings/cli.py`: add `init`, `update`, `dry-run`, `solution`, and `--debug`.
- Modify `pyproject.toml`: package curriculum resources and add build/test dependencies used by release verification.
- Create `tests/unit/test_curriculum.py`: packaged curriculum and workspace-copy tests.
- Extend `tests/integration/`: CLI init/update/reset/runner/package-flow tests.
- Create `solutions/`: mirrored reference answers, one file per exercise.
- Create `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`.
- Modify `.github/workflows/ci.yml`: add package install smoke test.
- Create `.github/workflows/publish.yml`: trusted PyPI/GitHub release workflow, disabled until credentials are configured.

## Phase 0: Branch And Baseline

### Task 0: Prepare Implementation Branch

**Files:**
- No code files changed.

- [ ] **Step 1: Confirm clean working tree**

Run:

```bash
git status --short
```

Expected: no output, or only files intentionally kept from previous work. If unrelated changes exist, stash or commit them before starting.

- [ ] **Step 2: Create the feature branch**

Run:

```bash
git switch -c feature/product-maturity
```

Expected: `Switched to a new branch 'feature/product-maturity'`.

- [ ] **Step 3: Run baseline verification**

Run:

```bash
python -m pytest -q
pylings --root tests/fixtures/passing_curriculum verify
python -m pylings --version
```

Expected: all tests pass, fixture verify exits `0`, version prints the current package version.

- [ ] **Step 4: Commit baseline marker**

Run:

```bash
git commit --allow-empty -m "chore: start product maturity work"
```

Expected: one empty commit marking the branch start.

## Phase 1: Self-Contained Distribution

### Task 1: Add Packaged Curriculum API

**Files:**
- Create: `pylings/core/curriculum.py`
- Test: `tests/unit/test_curriculum.py`
- Modify: `pyproject.toml`

- [ ] **Step 1: Write failing curriculum tests**

Create `tests/unit/test_curriculum.py`:

```python
from pathlib import Path

from pylings.core import curriculum


def test_source_root_finds_curriculum_files():
    root = curriculum.source_root()

    assert (root / "info.toml").exists()
    assert (root / "exercises").is_dir()
    assert (root / "checks").is_dir()


def test_init_workspace_copies_curriculum(tmp_path):
    target = tmp_path / "workspace"

    result = curriculum.init_workspace(target)

    assert result == target
    assert (target / "info.toml").exists()
    assert (target / "exercises").is_dir()
    assert (target / "checks").is_dir()
    assert (target / ".pylings" / "originals").is_dir()
    assert (target / ".gitignore").read_text(encoding="utf-8").splitlines() == [
        ".pylings/state.json",
        ".pylings_debug.log",
        "__pycache__/",
        "*.pyc",
    ]


def test_init_workspace_refuses_non_empty_directory(tmp_path):
    target = tmp_path / "workspace"
    target.mkdir()
    (target / "notes.txt").write_text("keep me", encoding="utf-8")

    try:
        curriculum.init_workspace(target)
    except curriculum.WorkspaceError as exc:
        assert "already exists and is not empty" in str(exc)
    else:
        raise AssertionError("expected WorkspaceError")


def test_update_workspace_preserves_user_exercise_edit(tmp_path):
    target = curriculum.init_workspace(tmp_path / "workspace")
    exercise = next((target / "exercises").rglob("*.py"))
    exercise.write_text("# user edit\n", encoding="utf-8")

    curriculum.update_workspace(target)

    assert exercise.read_text(encoding="utf-8") == "# user edit\n"
    assert (target / "checks").is_dir()
    assert (target / ".pylings" / "originals" / exercise.name).exists()
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
python -m pytest tests/unit/test_curriculum.py -q
```

Expected: import or attribute failure because `pylings.core.curriculum` does not exist yet.

- [ ] **Step 3: Implement curriculum helpers**

Create `pylings/core/curriculum.py`:

```python
from __future__ import annotations

import shutil
from importlib import resources
from importlib.abc import Traversable
from pathlib import Path


class WorkspaceError(RuntimeError):
    """Workspace init or update failed."""


MANAGED_DIRS = ("checks",)
CURRICULUM_DIRS = ("exercises", "checks")
GITIGNORE_LINES = [
    ".pylings/state.json",
    ".pylings_debug.log",
    "__pycache__/",
    "*.pyc",
]


def source_root() -> Path:
    """Return the curriculum source root for editable and wheel installs."""
    packaged = resources.files("pylings").joinpath("curriculum")
    if packaged.joinpath("info.toml").is_file():
        return Path(str(packaged))

    repo_root = Path(__file__).resolve().parents[2]
    if (repo_root / "info.toml").exists():
        return repo_root

    raise WorkspaceError("packaged curriculum not found")


def _copy_path(src: Path, dst: Path, *, overwrite: bool) -> None:
    if src.is_dir():
        if dst.exists() and overwrite:
            shutil.rmtree(dst)
        dst.mkdir(parents=True, exist_ok=True)
        for child in src.iterdir():
            _copy_path(child, dst / child.name, overwrite=overwrite)
        return

    if dst.exists() and not overwrite:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _write_workspace_gitignore(root: Path) -> None:
    (root / ".gitignore").write_text(
        "\n".join(GITIGNORE_LINES) + "\n",
        encoding="utf-8",
    )


def _sync_originals(root: Path, src_root: Path) -> None:
    originals = root / ".pylings" / "originals"
    if originals.exists():
        shutil.rmtree(originals)
    for exercise in (src_root / "exercises").rglob("*.py"):
        rel = exercise.relative_to(src_root / "exercises")
        target = originals / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(exercise, target)


def init_workspace(path: Path, *, force: bool = False) -> Path:
    path = path.expanduser().resolve()
    if path.exists() and any(path.iterdir()) and not force:
        raise WorkspaceError(f"{path} already exists and is not empty")
    path.mkdir(parents=True, exist_ok=True)

    src_root = source_root()
    _copy_path(src_root / "info.toml", path / "info.toml", overwrite=True)
    for dirname in CURRICULUM_DIRS:
        _copy_path(src_root / dirname, path / dirname, overwrite=True)
    _sync_originals(path, src_root)
    _write_workspace_gitignore(path)
    return path


def update_workspace(path: Path) -> Path:
    path = path.expanduser().resolve()
    if not (path / "info.toml").exists():
        raise WorkspaceError(f"{path} is not a pylings workspace")

    src_root = source_root()
    _copy_path(src_root / "info.toml", path / "info.toml", overwrite=True)
    _copy_path(src_root / "checks", path / "checks", overwrite=True)
    _copy_path(src_root / "exercises", path / "exercises", overwrite=False)
    _sync_originals(path, src_root)
    _write_workspace_gitignore(path)
    return path
```

- [ ] **Step 4: Include curriculum in built wheels**

Modify `pyproject.toml`:

```toml
[tool.hatch.build.targets.wheel.force-include]
"pylings/pylings.tcss" = "pylings/pylings.tcss"
"pylings/docs" = "pylings/docs"
"info.toml" = "pylings/curriculum/info.toml"
"exercises" = "pylings/curriculum/exercises"
"checks" = "pylings/curriculum/checks"
```

- [ ] **Step 5: Run curriculum tests**

Run:

```bash
python -m pytest tests/unit/test_curriculum.py -q
```

Expected: all curriculum tests pass.

- [ ] **Step 6: Commit**

Run:

```bash
git add pyproject.toml pylings/core/curriculum.py tests/unit/test_curriculum.py
git commit -m "feat: package curriculum resources"
```

## Phase 2: Workspace Lifecycle CLI

### Task 2: Add `init` And `update` Commands

**Files:**
- Modify: `pylings/cli.py`
- Test: `tests/integration/test_cli_workspace.py`

- [ ] **Step 1: Write failing CLI tests**

Create `tests/integration/test_cli_workspace.py`:

```python
from pathlib import Path

from pylings.cli import main


def test_init_command_creates_workspace(tmp_path):
    target = tmp_path / "learn-python"

    code = main(["init", "--path", str(target)])

    assert code == 0
    assert (target / "info.toml").exists()
    assert (target / "exercises").is_dir()
    assert (target / "checks").is_dir()


def test_init_command_requires_force_for_non_empty_directory(tmp_path, capsys):
    target = tmp_path / "learn-python"
    target.mkdir()
    (target / "notes.txt").write_text("keep", encoding="utf-8")

    code = main(["init", "--path", str(target)])

    assert code == 1
    assert "already exists and is not empty" in capsys.readouterr().err


def test_update_command_preserves_user_exercises(tmp_path):
    target = tmp_path / "learn-python"
    assert main(["init", "--path", str(target)]) == 0
    exercise = next((target / "exercises").rglob("*.py"))
    exercise.write_text("# edited\n", encoding="utf-8")

    code = main(["update", "--path", str(target)])

    assert code == 0
    assert exercise.read_text(encoding="utf-8") == "# edited\n"
    assert (target / ".pylings" / "originals").is_dir()
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
python -m pytest tests/integration/test_cli_workspace.py -q
```

Expected: parser rejects `init` and `update`.

- [ ] **Step 3: Add parser entries**

Modify `_build_parser()` in `pylings/cli.py`:

```python
p_init = sub.add_parser("init", help="Create a pylings workspace.")
p_init.add_argument("--path", type=Path, default=Path.cwd())
p_init.add_argument("--force", action="store_true", help="Overwrite managed workspace files.")

p_update = sub.add_parser("update", help="Update an existing pylings workspace.")
p_update.add_argument("--path", type=Path, default=Path.cwd())
```

- [ ] **Step 4: Add command handlers**

Add to `pylings/cli.py`:

```python
def _cmd_init(path: Path, force: bool) -> int:
    from pylings.core.curriculum import WorkspaceError, init_workspace

    try:
        root = init_workspace(path, force=force)
    except WorkspaceError as e:
        sys.stderr.write(f"pylings: {e}\n")
        return 1
    print(f"initialized: {root}")
    return 0


def _cmd_update(path: Path) -> int:
    from pylings.core.curriculum import WorkspaceError, update_workspace

    try:
        root = update_workspace(path)
    except WorkspaceError as e:
        sys.stderr.write(f"pylings: {e}\n")
        return 1
    print(f"updated: {root}")
    return 0
```

Route before `_snapshot_all(args.root)` because these commands do not need an existing manifest:

```python
if args.command == "init":
    return _cmd_init(args.path, args.force)
if args.command == "update":
    return _cmd_update(args.path)
```

- [ ] **Step 5: Run CLI workspace tests**

Run:

```bash
python -m pytest tests/integration/test_cli_workspace.py -q
```

Expected: all workspace CLI tests pass.

- [ ] **Step 6: Commit**

Run:

```bash
git add pylings/cli.py tests/integration/test_cli_workspace.py
git commit -m "feat: add workspace init and update commands"
```

### Task 3: Make Reset Restore True Pristine Sources

**Files:**
- Modify: `pylings/core/exercise.py`
- Modify: `pylings/core/manifest.py`
- Modify: `pylings/core/reset.py`
- Modify: `pylings/cli.py`
- Test: `tests/unit/test_reset.py`
- Test: `tests/integration/test_cli_reset.py`

- [ ] **Step 1: Add failing reset test**

Append to `tests/unit/test_reset.py`:

```python
from pylings.core.curriculum import init_workspace
from pylings.core.manifest import load
from pylings.core.reset import restore


def test_restore_uses_pristine_originals_not_current_file(tmp_path):
    root = init_workspace(tmp_path / "workspace")
    manifest = load(root)
    exercise = manifest.exercises[0]
    pristine = (root / ".pylings" / "originals" / exercise.rel_path.relative_to("exercises")).read_text(
        encoding="utf-8"
    )
    exercise.path.write_text("# corrupted user edit\n", encoding="utf-8")

    restore(root, exercise)

    assert exercise.path.read_text(encoding="utf-8") == pristine
```

- [ ] **Step 2: Run the reset test to verify failure**

Run:

```bash
python -m pytest tests/unit/test_reset.py::test_restore_uses_pristine_originals_not_current_file -q
```

Expected: failure because `Exercise` has no `rel_path` and reset uses first-seen snapshots.

- [ ] **Step 3: Add exercise path metadata**

Modify `pylings/core/exercise.py`:

```python
@dataclass(frozen=True)
class Exercise:
    name: str
    path: Path
    check_path: Path
    topic: str
    hint: str
    docs: str = ""
    root: Path | None = None
    rel_path: Path | None = None
    check_rel_path: Path | None = None
```

Modify the `Exercise(...)` construction in `pylings/core/manifest.py`:

```python
Exercise(
    name=name,
    path=abs_path,
    check_path=check_abs,
    topic=rel_path.parent.name,
    hint=entry.get("hint", ""),
    docs=entry.get("docs", ""),
    root=root,
    rel_path=rel_path,
    check_rel_path=check_rel,
)
```

- [ ] **Step 4: Replace reset restore implementation**

Modify `pylings/core/reset.py`:

```python
def _original_path(root: Path, exercise: Exercise) -> Path:
    if exercise.rel_path is None:
        return _snapshot_path(root, exercise)
    return root / ".pylings" / "originals" / exercise.rel_path.relative_to("exercises")


def restore(root: Path, exercise: Exercise) -> None:
    """Overwrite the exercise file with its pristine packaged original."""
    original = _original_path(root, exercise)
    if not original.exists():
        raise ResetError(
            f"no pristine original for {exercise.name!r}. Run 'pylings update' first."
        )
    shutil.copy2(original, exercise.path)
```

- [ ] **Step 5: Stop snapshotting every command**

Modify `main()` in `pylings/cli.py` by removing the `_snapshot_all(args.root)` block. Keep `_snapshot_all()` temporarily only if existing tests still import it; otherwise delete it in a follow-up cleanup commit.

- [ ] **Step 6: Run reset and CLI tests**

Run:

```bash
python -m pytest tests/unit/test_reset.py tests/integration/test_cli_reset.py tests/integration/test_cli_workspace.py -q
```

Expected: all reset/workspace tests pass.

- [ ] **Step 7: Commit**

Run:

```bash
git add pylings/core/exercise.py pylings/core/manifest.py pylings/core/reset.py pylings/cli.py tests/unit/test_reset.py tests/integration/test_cli_reset.py
git commit -m "fix: restore exercises from pristine originals"
```

## Phase 3: Runner And CLI Maturity

### Task 4: Improve Runner Filenames, cwd, And Debug Output

**Files:**
- Modify: `pylings/core/runner.py`
- Test: `tests/unit/test_runner.py`

- [ ] **Step 1: Add failing runner tests**

Append to `tests/unit/test_runner.py`:

```python
from pylings.core.exercise import Exercise
from pylings.core.runner import run


def test_runner_uses_exercise_directory_for_relative_files(tmp_path):
    exercise_path = tmp_path / "exercise.py"
    check_path = tmp_path / "check.py"
    data_path = tmp_path / "data.txt"
    data_path.write_text("pylings\n", encoding="utf-8")
    exercise_path.write_text(
        "value = open('data.txt', encoding='utf-8').read().strip()\n",
        encoding="utf-8",
    )
    check_path.write_text("assert value == 'pylings'\n", encoding="utf-8")

    result = run(Exercise("relative", exercise_path, check_path, "x", "", root=tmp_path))

    assert result.passed is True


def test_runner_traceback_mentions_real_exercise_file(tmp_path):
    exercise_path = tmp_path / "exercise.py"
    check_path = tmp_path / "check.py"
    exercise_path.write_text("raise RuntimeError('boom')\n", encoding="utf-8")
    check_path.write_text("assert True\n", encoding="utf-8")

    result = run(Exercise("traceback", exercise_path, check_path, "x", "", root=tmp_path))

    assert result.passed is False
    assert str(exercise_path) in result.stderr
```

- [ ] **Step 2: Run runner tests to verify failure**

Run:

```bash
python -m pytest tests/unit/test_runner.py::test_runner_uses_exercise_directory_for_relative_files tests/unit/test_runner.py::test_runner_traceback_mentions_real_exercise_file -q
```

Expected: relative file test fails because cwd is not set, traceback test mentions a temp file.

- [ ] **Step 3: Replace temp-file concatenation with compiled source wrapper**

Modify `run()` in `pylings/core/runner.py` so the temporary script compiles each source with its real filename:

```python
runner_src = f"""
from pathlib import Path

namespace = {{}}
exercise_src = Path({str(exercise.path)!r}).read_text(encoding="utf-8")
check_src = Path({str(exercise.check_path)!r}).read_text(encoding="utf-8")
exec(compile(exercise_src, {str(exercise.path)!r}, "exec"), namespace)
exec(compile(check_src, {str(exercise.check_path)!r}, "exec"), namespace)
"""
```

Pass cwd into `subprocess.run()`:

```python
cwd = exercise.root or exercise.path.parent
proc = subprocess.run(
    [sys.executable, tmp.name],
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
    timeout=timeout_s,
    env=env,
    cwd=cwd,
)
```

- [ ] **Step 4: Run runner tests**

Run:

```bash
python -m pytest tests/unit/test_runner.py -q
```

Expected: all runner tests pass.

- [ ] **Step 5: Commit**

Run:

```bash
git add pylings/core/runner.py tests/unit/test_runner.py
git commit -m "fix: run exercises with workspace cwd and real tracebacks"
```

### Task 5: Add `dry-run`, `solution`, And `--debug`

**Files:**
- Modify: `pylings/cli.py`
- Modify: `pylings/core/runner.py`
- Create: `pylings/core/solutions.py`
- Create: `solutions/.keep`
- Test: `tests/integration/test_cli_dry_run.py`
- Test: `tests/integration/test_cli_solution.py`

- [ ] **Step 1: Write failing CLI tests**

Create `tests/integration/test_cli_dry_run.py`:

```python
from pylings.cli import main


def test_dry_run_alias_runs_one_exercise(tmp_path):
    code = main(["--root", "tests/fixtures/passing_curriculum", "dry-run", "passing1"])

    assert code == 0
```

Create `tests/integration/test_cli_solution.py`:

```python
from pathlib import Path

from pylings.cli import main


def test_solution_command_runs_workspace_solution(tmp_path):
    root = tmp_path / "workspace"
    (root / "solutions").mkdir(parents=True)
    (root / "checks").mkdir()
    (root / "exercises").mkdir()
    (root / "info.toml").write_text(
        '''
format_version = 1

[[exercises]]
name = "passing1"
path = "exercises/passing1.py"
hint = "set x"
docs = "https://docs.python.org/3/"
''',
        encoding="utf-8",
    )
    (root / "exercises" / "passing1.py").write_text("x = 0\n", encoding="utf-8")
    (root / "solutions" / "passing1.py").write_text("x = 1\n", encoding="utf-8")
    (root / "checks" / "passing1.py").write_text("assert x == 1\n", encoding="utf-8")

    code = main(["--root", str(root), "solution", "passing1"])

    assert code == 0
```

- [ ] **Step 2: Run tests to verify failure**

Run:

```bash
python -m pytest tests/integration/test_cli_dry_run.py tests/integration/test_cli_solution.py -q
```

Expected: parser rejects both commands.

- [ ] **Step 3: Add solutions resolver**

Create `pylings/core/solutions.py`:

```python
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from pylings.core.exercise import Exercise


class SolutionError(RuntimeError):
    """Solution lookup failed."""


def solution_exercise(root: Path, exercise: Exercise) -> Exercise:
    path = root / "solutions" / f"{exercise.name}.py"
    if not path.exists():
        raise SolutionError(f"no solution for {exercise.name!r}")
    return replace(exercise, path=path, rel_path=Path("solutions") / path.name)
```

- [ ] **Step 4: Add CLI commands**

In `_build_parser()`:

```python
p_dry_run = sub.add_parser("dry-run", help="Run one exercise non-interactively.")
p_dry_run.add_argument("name")

p_solution = sub.add_parser("solution", aliases=["sol"], help="Run a reference solution.")
p_solution.add_argument("name")

parser.add_argument("--debug", action="store_true", help="Write debug output to .pylings_debug.log.")
```

In `main()`:

```python
if args.command == "dry-run":
    return _cmd_run(args.root, args.name)
if args.command in {"solution", "sol"}:
    return _cmd_solution(args.root, args.name)
```

Add handler:

```python
def _cmd_solution(root: Path, name: str) -> int:
    from pylings.core.manifest import load as load_manifest
    from pylings.core.runner import run_verify
    from pylings.core.solutions import SolutionError, solution_exercise

    manifest = load_manifest(root)
    try:
        ex = solution_exercise(root, manifest.by_name(name))
    except (KeyError, SolutionError) as e:
        sys.stderr.write(f"pylings: {e}\n")
        return 1

    result = run_verify(ex)
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return 0 if result.passed else 1
```

- [ ] **Step 5: Add debug log behavior**

In `main()`, after parsing:

```python
if getattr(args, "debug", False):
    (args.root / ".pylings_debug.log").write_text(
        f"argv={argv if argv is not None else sys.argv[1:]!r}\n",
        encoding="utf-8",
    )
```

- [ ] **Step 6: Run command tests**

Run:

```bash
python -m pytest tests/integration/test_cli_dry_run.py tests/integration/test_cli_solution.py -q
```

Expected: all command tests pass.

- [ ] **Step 7: Commit**

Run:

```bash
git add pylings/cli.py pylings/core/solutions.py tests/integration/test_cli_dry_run.py tests/integration/test_cli_solution.py solutions/.keep
git commit -m "feat: add dry-run and solution commands"
```

## Phase 4: Curriculum Content And Learner Experience

### Task 6: Add Solution Coverage Gate

**Files:**
- Create: `tests/unit/test_solution_coverage.py`
- Add: `solutions/<exercise-name>.py` for every exercise listed in `info.toml`

- [ ] **Step 1: Add coverage test**

Create `tests/unit/test_solution_coverage.py`:

```python
from pathlib import Path

import tomllib


def test_every_exercise_has_solution_file():
    root = Path(__file__).resolve().parents[2]
    data = tomllib.loads((root / "info.toml").read_text(encoding="utf-8"))
    missing = [
        entry["name"]
        for entry in data["exercises"]
        if not (root / "solutions" / f"{entry['name']}.py").exists()
    ]

    assert missing == []
```

- [ ] **Step 2: Run coverage test**

Run:

```bash
python -m pytest tests/unit/test_solution_coverage.py -q
```

Expected: failure listing every exercise without a solution.

- [ ] **Step 3: Add solution files topic by topic**

For each exercise in `info.toml`, create `solutions/<exercise-name>.py` that passes its mirrored check. Validate each topic before moving on:

```bash
python -m pylings --root . solution variables1
python -m pylings --root . solution variables2
python -m pylings --root . solution variables3
```

Expected: every solution command exits `0`. Repeat the command pattern for each exercise name in the topic until the coverage test passes.

- [ ] **Step 4: Run full solution verification**

Run:

```bash
python -m pytest tests/unit/test_solution_coverage.py -q
python -m pytest tests/integration/test_cli_solution.py -q
```

Expected: all solution tests pass.

- [ ] **Step 5: Commit**

Run:

```bash
git add solutions tests/unit/test_solution_coverage.py
git commit -m "feat: add reference solutions"
```

### Task 7: Add External File Watch Mode

**Files:**
- Modify: `pyproject.toml`
- Create: `pylings/core/watcher.py`
- Modify: `pylings/cli.py`
- Test: `tests/unit/test_watcher.py`

- [ ] **Step 1: Add watchdog dependency**

Modify `pyproject.toml`:

```toml
dependencies = [
    "textual[syntax]>=8.0.0",
    "watchdog>=6.0.0",
]
```

- [ ] **Step 2: Add watcher smoke test**

Create `tests/unit/test_watcher.py`:

```python
from pylings.core.watcher import changed_python_file


def test_changed_python_file_accepts_exercise_file():
    assert changed_python_file("exercises/variables/variables1.py") is True


def test_changed_python_file_ignores_bytecode():
    assert changed_python_file("exercises/variables/__pycache__/variables1.pyc") is False
```

- [ ] **Step 3: Implement watcher filter**

Create `pylings/core/watcher.py`:

```python
from __future__ import annotations


def changed_python_file(path: str) -> bool:
    return path.endswith(".py") and "__pycache__" not in path
```

- [ ] **Step 4: Add CLI flag for later TUI integration**

In `_build_parser()`, add:

```python
parser.add_argument(
    "--watch-files",
    action="store_true",
    help="Rerun checks when exercise files change outside the TUI.",
)
```

Pass `watch_files=getattr(args, "watch_files", False)` into `run_tui()` after adding that optional parameter to `pylings/app.py`.

- [ ] **Step 5: Run watcher tests**

Run:

```bash
python -m pytest tests/unit/test_watcher.py -q
```

Expected: watcher filter tests pass.

- [ ] **Step 6: Commit**

Run:

```bash
git add pyproject.toml pylings/core/watcher.py pylings/cli.py pylings/app.py tests/unit/test_watcher.py
git commit -m "feat: add external file watch foundation"
```

## Phase 5: Packaging, CI, And Governance

### Task 8: Add Installed-Wheel Smoke Test

**Files:**
- Modify: `.github/workflows/ci.yml`
- Create: `tests/integration/test_installed_package.py`

- [ ] **Step 1: Add local package smoke test**

Create `tests/integration/test_installed_package.py`:

```python
from pylings.cli import main


def test_installed_package_can_initialize_and_list_workspace(tmp_path):
    root = tmp_path / "workspace"

    assert main(["init", "--path", str(root)]) == 0
    assert main(["--root", str(root), "list"]) == 0
```

- [ ] **Step 2: Add CI package commands**

Modify `.github/workflows/ci.yml`:

```yaml
      - run: python -m pip install build
      - run: python -m build
      - run: python -m pip install --force-reinstall dist/*.whl
      - run: pylings init --path /tmp/pylings-workspace
      - run: pylings --root /tmp/pylings-workspace list
```

- [ ] **Step 3: Run local verification**

Run:

```bash
python -m pytest tests/integration/test_installed_package.py -q
python -m build
python -m pip install --force-reinstall dist/*.whl
pylings init --path /tmp/pylings-smoke --force
pylings --root /tmp/pylings-smoke list
```

Expected: all commands exit `0`; list prints topic progress.

- [ ] **Step 4: Commit**

Run:

```bash
git add .github/workflows/ci.yml tests/integration/test_installed_package.py
git commit -m "ci: verify installed wheel workflow"
```

### Task 9: Add Governance Docs

**Files:**
- Create: `CONTRIBUTING.md`
- Create: `SECURITY.md`
- Create: `CODE_OF_CONDUCT.md`
- Create: `.github/pull_request_template.md`
- Create: `.github/ISSUE_TEMPLATE/bug_report.md`
- Create: `.github/ISSUE_TEMPLATE/feature_request.md`

- [ ] **Step 1: Add contributor guide**

Create `CONTRIBUTING.md`:

````markdown
# Contributing

## Development Setup

```bash
pip install -e ".[dev]"
python -m pytest -q
```

## Curriculum Changes

Update `info.toml`, `exercises/`, `checks/`, and `solutions/` together. Exercise and check paths must mirror each other.

## Pull Requests

Use focused branches named `feature/<name>` or `fix/<name>`. Include a short description, test output, and screenshots for TUI changes.
````

- [ ] **Step 2: Add security policy**

Create `SECURITY.md`:

```markdown
# Security Policy

Report security issues privately through GitHub Security Advisories. Do not open public issues for vulnerabilities.

Supported versions: latest released `0.x` version and current `main`.
```

- [ ] **Step 3: Add code of conduct**

Create `CODE_OF_CONDUCT.md`:

```markdown
# Code of Conduct

Pylings follows the Contributor Covenant Code of Conduct, version 2.1.

## Our Standards

Use welcoming and inclusive language, respect different experience levels, accept constructive feedback, and focus on what is best for the community.

Unacceptable behavior includes harassment, personal attacks, sexualized language or imagery, publishing private information, or sustained disruption of project work.

## Enforcement

Report unacceptable behavior through GitHub Security Advisories. Maintainers may remove comments, close issues, block users, or take other appropriate action.
```

- [ ] **Step 4: Add PR template**

Create `.github/pull_request_template.md`:

```markdown
## Summary

## Tests

## Screenshots

## Checklist

- [ ] Updated docs when behavior changed
- [ ] Added or updated tests
- [ ] Verified `python -m pytest -q`
```

- [ ] **Step 5: Add issue templates**

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug report
about: Report a reproducible problem
labels: bug
---

## What happened?

## Steps to reproduce

## Expected behavior

## Environment

- OS:
- Python:
- Terminal:
- Pylings version:
```

Create `.github/ISSUE_TEMPLATE/feature_request.md`:

```markdown
---
name: Feature request
about: Suggest an improvement
labels: enhancement
---

## Problem

## Proposed behavior

## Alternatives considered
```

- [ ] **Step 6: Commit**

Run:

```bash
git add CONTRIBUTING.md SECURITY.md CODE_OF_CONDUCT.md .github
git commit -m "docs: add contributor governance"
```

### Task 10: Fix Versioning And Release Automation

**Files:**
- Modify: `pyproject.toml`
- Modify: `pylings/cli.py`
- Modify: `Readme.md`
- Modify: `CHANGELOG.md`
- Create: `.github/workflows/publish.yml`

- [ ] **Step 1: Choose version format**

Use strict SemVer from the next release onward:

```toml
version = "0.1.0"
```

CLI version should match:

```python
__version__ = "0.1.0"
```

README release tags should use:

```text
feature/<name> -> dev -> main -> vMAJOR.MINOR.PATCH
```

- [ ] **Step 2: Add publish workflow**

Create `.github/workflows/publish.yml`:

```yaml
name: publish

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python -m pip install build
      - run: python -m build
      - uses: pypa/gh-action-pypi-publish@release/v1
```

- [ ] **Step 3: Run release verification**

Run:

```bash
python -m pytest -q
python -m build
python -m pip install --force-reinstall dist/*.whl
python -m pylings --version
```

Expected: tests pass, wheel builds, installed CLI prints `pylings 0.1.0`.

- [ ] **Step 4: Commit**

Run:

```bash
git add pyproject.toml pylings/cli.py Readme.md CHANGELOG.md .github/workflows/publish.yml
git commit -m "chore: align release automation with semver"
```

## Phase 6: Final Verification And Merge

### Task 11: Full Verification

**Files:**
- No code files changed unless verification reveals a bug.

- [ ] **Step 1: Run full local test suite**

Run:

```bash
python -m pytest -q
```

Expected: all tests pass.

- [ ] **Step 2: Verify workspace lifecycle manually**

Run:

```bash
rm -rf /tmp/pylings-manual
pylings init --path /tmp/pylings-manual
pylings --root /tmp/pylings-manual list
pylings --root /tmp/pylings-manual run variables1
pylings --root /tmp/pylings-manual reset variables1 --yes
pylings update --path /tmp/pylings-manual
```

Expected: init/list/reset/update exit `0`; `run variables1` may exit `1` if the exercise is intentionally incomplete, but it must print a useful learner-facing failure.

- [ ] **Step 3: Verify built wheel**

Run:

```bash
rm -rf dist /tmp/pylings-wheel
python -m build
python -m pip install --force-reinstall dist/*.whl
pylings init --path /tmp/pylings-wheel
pylings --root /tmp/pylings-wheel list
```

Expected: installed wheel can initialize and list a workspace outside the repository.

- [ ] **Step 4: Merge branch**

Run:

```bash
git switch dev
git merge --no-ff feature/product-maturity -m "merge: product maturity workflow"
python -m pytest -q
git switch main
git merge --no-ff dev -m "merge: release product maturity workflow"
```

Expected: merges succeed and tests pass on `dev` before merging to `main`.

- [ ] **Step 5: Tag release**

For strict SemVer:

```bash
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin dev main v0.1.0
```

If keeping the existing preview tag style:

```bash
git tag -a v0.1 -m "Release v0.1"
git push origin dev main v0.1
```

Expected: GitHub Actions runs CI on `main`; release publication should only happen after the GitHub Release is manually published.

## Self-Review

- Spec coverage: covers installability, init/update, reset correctness, runner robustness, richer CLI commands, solutions, watcher foundation, CI packaging, governance, and version/release policy.
- Placeholder scan: remaining content-heavy work is represented as a measurable coverage gate, not an undefined task.
- Type consistency: `Exercise.root`, `Exercise.rel_path`, and `Exercise.check_rel_path` are introduced before reset and runner tasks use them.
