# Changelog

All notable changes to this project are documented here. Pylings follows
Semantic Versioning.

## [0.2.0] - 2026-05-30

### Added

- Support for Python 3.9 and 3.10 (minimum was 3.11), broadening
  compatibility with stock macOS and Debian/Ubuntu interpreters.

### Changed

- The `type_hints4`, `type_hints8`, and `itertools8` exercises carry a small
  forward-compatibility shim (`from __future__ import annotations` and a
  `tee`-based `pairwise` fallback) so their modern syntax and stdlib usage run
  on Python 3.9 and 3.10. The learner's task is unchanged.

### Fixed

- Manifest loading now falls back to the `tomli` backport on Python < 3.11,
  where `tomllib` is not available in the standard library. Previously the
  package would install but crash on launch under older interpreters.

## [0.1.0] - 2026-05-25

### Added

- Interactive Textual coding workflow with topic picker, resume state, hints,
  reset, and automatic check reruns.
- CLI commands for listing topics, running exercises, printing hints, resetting
  files, and verifying curricula.
- 292 Python exercises across 31 topics with mirrored hidden checks.
- Bundled local Python documentation snippets generated from official docs.
- In-app documentation modal with `F5`, `Esc`, and `O` keyboard flow.
- PyPI distribution name `python-learnings`, which installs the `pylings` command.
- Contributor guide, screenshots, release flow notes, and MIT license.

### Verified

- Full test suite: `125 passed`.
- Curriculum/docs audit: every exercise has a configured docs URL and a bundled
  local snippet.
