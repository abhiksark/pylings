# Quick Start

## Install

Install the current release from GitHub:

```bash
pipx install "git+https://github.com/abhiksark/pylings.git@v0.1.0"
```

After PyPI publishing is enabled, the package install path will be:

```bash
pipx install python-learnings
```

The command installed by the package is `pylings`.

## Create A Workspace

```bash
pylings init --path ~/pylings-workspace
cd ~/pylings-workspace
pylings
```

`pylings init` copies exercises, hidden checks, reference solutions, and reset
snapshots into a learner workspace. Run `pylings` from that workspace to open
the first pending exercise.

## Useful Commands

```bash
pylings list
pylings topics
pylings hint variables1
pylings run variables1
pylings dry-run variables1
pylings reset variables1 --yes
pylings update
```

Use `pylings list` to inspect progress, `pylings hint <exercise>` for help, and
`pylings reset <exercise> --yes` to restore an exercise to its original broken
state.

## Exercise Loop

Each exercise contains a `# I AM NOT DONE` marker. Fix the code, remove the
marker, and let Pylings run the hidden check. Passing checks mark the exercise
complete and move the progress state forward.
