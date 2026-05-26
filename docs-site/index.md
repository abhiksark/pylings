# Pylings

Python learnings, Rustlings-style, in a live terminal TUI.

![Pylings terminal demo](https://raw.githubusercontent.com/abhiksark/pylings/main/docs/assets/demos/pylings-demo.gif)

Pylings helps learners practice Python by fixing small broken programs and
watching checks rerun as they work. The project includes 292 exercises across
31 topics, hidden pytest-style checks, a Textual editor, progressive hints, and
bundled Python documentation snippets for offline-friendly practice.

## Start Here

```bash
pipx install "git+https://github.com/abhiksark/pylings.git@v0.1.0"
pylings init --path ~/pylings-workspace
cd ~/pylings-workspace
pylings
```

The package name reserved for PyPI publishing is `python-learnings`. Until the
PyPI release is live, install the stable v0.1.0 release from the GitHub tag.

## What You Get

- Rustlings-inspired Python coding practice in the terminal.
- Live exercise verification while editing.
- Topic picker, progress tracking, reset, hints, and one-shot CLI commands.
- Local docs window with links back to the official Python documentation.
- A self-contained learner workspace created by `pylings init`.

## Project Status

Pylings is currently `v0.1.0` alpha. The public API, CLI, and curriculum are
usable, but the project is still hardening packaging, docs, first-run flow, and
release automation.
