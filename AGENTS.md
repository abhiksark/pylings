# Repository Guidelines

## Project Structure & Module Organization

`pythonlings/` contains the installable application package. Core exercise loading, workspace setup, state, reset, solutions, and runner logic live in `pythonlings/core/`; CLI entry points are in `pythonlings/cli.py` and `pythonlings/__main__.py`; Textual screens/widgets live in `pythonlings/screens/` and `pythonlings/widgets/`; `pythonlings/pythonlings.tcss` holds TUI styles.

Curriculum files are split between `exercises/<topic>/<exercise>.py` for learner code, `checks/<topic>/<exercise>.py` for hidden assertions, and `solutions/<exercise>.py` for reference answers. Keep these trees aligned with `info.toml`, which defines order, hints, and docs URLs. Tests live in `tests/unit/`, `tests/integration/`, and `tests/tui/`, with fixtures in `tests/fixtures/`.

## Build, Test, and Development Commands

- `pip install -e ".[dev]"`: install pythonlings locally with pytest dependencies.
- `pythonlings init --path ./learn-python`: create a self-contained learner workspace.
- `pythonlings`, `pythonlings topics`, `pythonlings list`: launch the TUI or inspect progress.
- `pythonlings run variables1`, `pythonlings dry-run variables1`, `pythonlings solution variables1`: test exercise and solution flows.
- `pythonlings --root tests/fixtures/passing_curriculum verify`: smoke-test a known passing fixture.
- `python -m pytest -q`: run the full suite configured in `pyproject.toml`.
- `python -m build`: build source and wheel distributions.

## Coding Style & Naming Conventions

Use Python 3.11+ idioms and 4-space indentation. Prefer small, typed functions where practical. Keep UI behavior in `screens` or `widgets`; keep filesystem, manifest, reset, and runner behavior in `core`. Name tests `test_<behavior>.py` and test functions `test_<expected_behavior>`. Curriculum names use topic plus ordinal, such as `variables1.py` or `collections10.py`.

## Testing Guidelines

Use pytest for all tests; async tests are supported by `pytest-asyncio` in auto mode. Add unit tests for core behavior, integration tests for CLI/workspace flows, and TUI tests for Textual interactions. When changing curriculum, update `exercises/`, `checks/`, `solutions/`, and `info.toml`, then run relevant pytest files plus `pythonlings --root tests/fixtures/passing_curriculum verify`.

## Commit & Pull Request Guidelines

Recent history uses conventional prefixes such as `feat:`, `fix:`, `docs:`, `chore:`, and merge commits between `feature/*`, `dev`, and `main`. Keep commits focused and imperative, for example `fix: reset exercise originals`. Pull requests should explain the user-facing change, list tests run, link issues when applicable, and include screenshots or terminal output for TUI/CLI changes.
