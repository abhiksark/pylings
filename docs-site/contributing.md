# Contributing

Read `AGENTS.md` for repository conventions and `CONTRIBUTING.md` for the
contributor workflow.

## Development Setup

```bash
git clone git@github.com:abhiksark/pythonlings.git
cd pythonlings
pip install -e ".[dev]"
python -m pytest -q
```

## Test Commands

```bash
python -m pytest -q
pythonlings --root tests/fixtures/passing_curriculum verify
python -m build
```

Use unit tests for core behavior, integration tests for CLI and workspace flows,
and TUI tests for Textual keyboard interactions.

## Curriculum Changes

Update these together:

```text
exercises/<topic>/<exercise>.py
checks/<topic>/<exercise>.py
solutions/<exercise>.py
info.toml
```

Keep exercise names stable and mirrored. Use topic-plus-number names such as
`variables1.py`, `collections10.py`, and `oop_advanced12.py`.
