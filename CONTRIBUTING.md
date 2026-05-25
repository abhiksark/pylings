# Contributing

## Development Setup

```bash
pip install -e ".[dev]"
python -m pytest -q
```

## Curriculum Changes

Update `info.toml`, `exercises/`, `checks/`, and `solutions/` together. Exercise and check paths must mirror each other, and every exercise must have a passing reference solution.

## Pull Requests

Use focused branches named `feature/<name>` or `fix/<name>`. Include a short description, test output, and screenshots for TUI changes.
