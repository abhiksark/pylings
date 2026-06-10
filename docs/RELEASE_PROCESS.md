# Release Process

Pythonlings uses a feature-branch workflow and Semantic Versioning.

## Branches

- `feature/<name>`: one focused change, such as `feature/local-docs`.
- `dev`: integration branch for reviewed feature work.
- `main`: release branch. Only verified `dev` snapshots are merged here.

## Versioning

Use `MAJOR.MINOR` release tags.

- Increment `MAJOR` for incompatible CLI, manifest, or curriculum changes.
- Increment `MINOR` for new exercises, topics, TUI features, or docs workflows.
- Increment `PATCH` for compatible fixes, documentation, packaging, and tests.

## Release Checklist

1. Merge feature branches into `dev` with reviewed, focused commits.
2. Run `python -m pytest -q`.
3. Run `pythonlings --root tests/fixtures/passing_curriculum verify`.
4. Update `CHANGELOG.md` and the version in `pythonlings/cli.py` and `pyproject.toml`.
5. Merge `dev` into `main`.
6. Create an annotated tag, for example `git tag -a v0.1 -m "Release v0.1"`.
7. Push `main`, `dev`, and tags.
