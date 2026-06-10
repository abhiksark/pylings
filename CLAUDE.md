# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Pythonlings is "Rustlings for Python": a terminal TUI (Textual) where learners fix small broken exercises and checks rerun on save. Published on PyPI as `pythonlings` (formerly `python-learnings`; the unrelated `pylings` PyPI name belongs to a different project).

## Commands

```bash
pip install -e ".[dev]"          # local install with pytest deps

python -m pytest -q                              # full suite
python -m pytest tests/unit/test_runner.py -q    # one file
python -m pytest tests/unit/test_state.py::test_name -q  # one test

pylings --root tests/fixtures/passing_curriculum verify   # smoke-test: all solutions pass their checks

python -m build                  # sdist + wheel
```

Manual testing of flows: `pylings init --path ./learn-python` (create a learner workspace), `pylings` (TUI), `pylings run variables1`, `pylings dry-run variables1`, `pylings solution variables1`, `pylings hint`, `pylings list`, `pylings topics`, `pylings reset`. `--root` points any command at an arbitrary workspace (used heavily by tests against `tests/fixtures/`).

## Architecture

Two distinct trees in this repo:

1. **The application** — `pylings/` (installable package)
2. **The curriculum** — repo-root `exercises/`, `checks/`, `solutions/`, and `info.toml`

At build time, hatch `force-include` maps the curriculum into the wheel as `pylings/curriculum/` (see `pyproject.toml`). `pylings init` copies that bundled curriculum into a self-contained learner workspace; progress lives in `<workspace>/.pylings/state.json` (written atomically, with `.bak` recovery on corruption).

### Curriculum model

Each exercise is a triple that must stay in sync, plus a manifest entry:

- `exercises/<topic>/<name>.py` — the broken code the learner edits, containing the `# I AM NOT DONE` marker (defined in `core/exercise.py`)
- `checks/<topic>/<name>.py` — hidden bare `assert` statements (not pytest)
- `solutions/<name>.py` — reference answer
- `info.toml` — ordered `[[exercises]]` entries with `name`, `path`, `hint`, `docs` URL; this file is the source of truth for exercise order and topics

When changing curriculum, update all four, then run the relevant tests plus `pylings --root tests/fixtures/passing_curriculum verify`. Exercise names are topic + ordinal (`variables1`, `collections10`).

### How checks run (`core/runner.py`)

An exercise passes when a generated runner script `exec()`s the exercise source and then the check source in a shared namespace, in a fresh subprocess with a 5s timeout. The check sees the exercise's variables directly — that's why checks are bare asserts. Passing checks alone aren't enough: the learner must also remove `# I AM NOT DONE` to advance.

### Layering

- `pylings/core/` — all filesystem, manifest, state, reset, solutions, runner, and watcher logic. No UI imports.
- `pylings/screens/` and `pylings/widgets/` — Textual UI only; `pylings/app.py` wires them up; `pylings.tcss` holds styles.
- `pylings/cli.py` — argparse subcommands; entry point `pylings = "pylings.cli:main"`.

Keep UI behavior in screens/widgets and behavior logic in core — tests depend on this split (`tests/unit/` for core, `tests/integration/` for CLI/workspace flows, `tests/tui/` for Textual pilot tests, fixtures in `tests/fixtures/`).

## Conventions

- `requires-python = ">=3.9"`: guard newer-stdlib usage (e.g. `tomllib` falls back to `tomli` in `core/manifest.py`); `from __future__ import annotations` at the top of modules.
- Async tests run under `pytest-asyncio` in auto mode (configured in `pyproject.toml`).
- Tests are named `test_<behavior>.py` / `test_<expected_behavior>`.
- Commits use conventional prefixes (`feat:`, `fix:`, `docs:`, `chore:`); work flows through `feature/*` → `dev` → `main`.
- `AGENTS.md` holds the same contributor guidelines in long form.
