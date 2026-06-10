# Contributing

Pythonlings is actively developed and **open to contributors** — beginners welcome.
The fastest way in is a [`good first issue`](https://github.com/abhiksark/pythonlings/issues?q=is%3Aopen+label%3A%22good+first+issue%22).

## Where the work is

- **[0.3.0 roadmap](docs/roadmap/0.3.0.md)** — the current focus (wider adoption
  for beginners). Each roadmap issue is written to be picked up cold: it has
  context, scope, the exact files to touch, and how to verify.
- Browse open issues by label: [`good first issue`](https://github.com/abhiksark/pythonlings/issues?q=is%3Aopen+label%3A%22good+first+issue%22),
  [`help wanted`](https://github.com/abhiksark/pythonlings/issues?q=is%3Aopen+label%3A%22help+wanted%22).

## Claiming an issue

1. Comment on the issue to claim it (e.g. "I'd like to take this"). This avoids
   two people doing the same work.
2. Ask any questions right on the issue — happy to clarify scope.
3. Open a PR that references the issue (`Closes #NN`).

No need to wait for a formal assignment; claiming by comment is enough.

## Development Setup

```bash
git clone git@github.com:abhiksark/pythonlings.git
cd pythonlings
pip install -e ".[dev]"   # or: uv pip install -e ".[dev]"
python -m pytest -q
```

Supported Python: 3.9+.

## Curriculum Changes

Update `info.toml`, `exercises/`, `checks/`, and `solutions/` together. Exercise
and check paths must mirror each other, and **every exercise must have a passing
reference solution** (`tests/integration/test_solution_verify.py` enforces this).

## Pull Requests

- Use focused branches named `feature/<name>` or `fix/<name>`.
- Reference the issue you're closing (`Closes #NN`).
- Include a short description, test output (`python -m pytest -q`), and
  screenshots/GIFs for TUI changes.
- Keep PRs scoped to one issue where possible.
