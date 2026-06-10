# Quick Start

## Install

Install the current release from GitHub:

```bash
pipx install "git+https://github.com/abhiksark/pythonlings.git@v0.1.0"
```

After PyPI publishing is enabled, the package install path will be:

```bash
pipx install pythonlings
```

The command installed by the package is `pythonlings`.

## Create A Workspace

```bash
pythonlings init --path ~/pythonlings-workspace
cd ~/pythonlings-workspace
pythonlings
```

`pythonlings init` copies exercises, hidden checks, reference solutions, and reset
snapshots into a learner workspace. Run `pythonlings` from that workspace to open
the first pending exercise.

## Useful Commands

```bash
pythonlings list
pythonlings topics
pythonlings hint variables1
pythonlings run variables1
pythonlings dry-run variables1
pythonlings reset variables1 --yes
pythonlings update
```

Use `pythonlings list` to inspect progress, `pythonlings hint <exercise>` for help, and
`pythonlings reset <exercise> --yes` to restore an exercise to its original broken
state.

## Exercise Loop

Each exercise contains a `# I AM NOT DONE` marker. Fix the code, remove the
marker, and let Pythonlings run the hidden check. Passing checks mark the exercise
complete and move the progress state forward.
