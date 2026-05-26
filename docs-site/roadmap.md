# Roadmap

Pylings is currently `v0.1.0` alpha. The core learner loop works, but the
project still needs product hardening before calling it stable.

## Current Release

- 292 exercises across 31 topics.
- Live Textual editor and automatic checks.
- Topic picker, progress state, reset, hints, and CLI commands.
- Bundled Python docs snippets with official docs links.
- GitHub install path for `v0.1.0`.

## Next Work

- Finish PyPI publishing for the `python-learnings` project name.
- Improve first-run onboarding and empty-state copy.
- Harden keyboard flow around `Enter`, `Esc`, `F4`, and `F5`.
- Add more TUI tests for the coding screen, docs window, and topic picker.
- Add a release smoke test that installs the built wheel and exercises the CLI.
- Continue auditing exercises for clearer hints and stronger hidden checks.

## Release Policy

Pylings follows Semantic Versioning.

- `MAJOR`: incompatible curriculum or CLI changes.
- `MINOR`: new topics, exercises, TUI features, or docs workflows.
- `PATCH`: fixes, copy edits, compatible tests, and packaging updates.
