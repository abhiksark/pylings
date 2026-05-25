# Repository Guidelines

## Project Structure & Module Organization

`pylings/` contains the installable application package. Core exercise loading, state, reset, and runner logic lives in `pylings/core/`; CLI entry points are in `pylings/cli.py` and `pylings/__main__.py`; Textual screens and widgets live in `pylings/screens/` and `pylings/widgets/`; `pylings/pylings.tcss` holds TUI styles.

Curriculum files are split between `exercises/<topic>/<exercise>.py` for learner-editable code and `checks/<topic>/<exercise>.py` for hidden assertions. Keep these trees mirrored. `info.toml` defines exercise order and hints. Tests are under `tests/unit/`, `tests/integration/`, and `tests/tui/`, with reusable sample curricula in `tests/fixtures/`.

## Build, Test, and Development Commands

- `pip install -e ".[dev]"`: install pylings locally with pytest dependencies.
- `pylings`: launch the Textual app in watch mode.
- `pylings list`, `pylings hint variables1`, `pylings run variables1`: exercise common CLI paths.
- `pylings --root tests/fixtures/passing_curriculum verify`: smoke-test curriculum verification against a known passing fixture.
- `pytest`: run the full test suite configured in `pyproject.toml`.
- `pytest tests/unit` or `pytest tests/integration/test_cli_run.py`: run focused tests while developing.
- `python -m build`: build distribution artifacts when the `build` package is available.

## Coding Style & Naming Conventions

Use Python 3.11+ idioms and standard 4-space indentation. Prefer small, typed functions where practical, and keep UI-specific behavior inside `screens` or `widgets` instead of `core`. Name tests `test_<behavior>.py` and test functions `test_<expected_behavior>`. Curriculum exercise/check filenames use the topic prefix plus an ordinal, such as `variables1.py` or `collections10.py`.

## Testing Guidelines

Use pytest for all tests; async tests are supported by `pytest-asyncio` with auto mode. Add unit tests for core behavior, integration tests for CLI flows, and TUI tests for Textual interactions. When adding or changing curriculum, update both `exercises/`, `checks/`, and `info.toml`, then run the verification fixture command plus relevant pytest files.

## Commit & Pull Request Guidelines

Recent history uses conventional prefixes such as `feat:`, `fix:`, and `docs:`. Keep commits focused and imperative, for example `fix: reset hints between exercises`. Pull requests should explain the user-facing change, list tests run, link related issues when applicable, and include screenshots or terminal output for TUI/CLI behavior changes.
