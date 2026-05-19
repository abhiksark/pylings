# Pylings

Rustlings, but for Python. A series of interactive exercises that teach Python by example — each ships with broken code and a `# I AM NOT DONE` marker. Fix it, save the file, watch the checks pass, advance to the next one.

## Install

```bash
pipx install pylings           # end users
# or, for contributors:
git clone <repo> pylings && cd pylings && pip install -e ".[dev]"
```

## Use

```bash
pylings                                # launches the TUI in watch mode
pylings list                           # shows every exercise with its status
pylings hint variables1                # prints the hint for an exercise
pylings run variables1                 # one-shot run, no TUI
pylings reset variables1               # restore original (asks y/N; --yes skips)
pylings --root <path> verify           # CI / curriculum-author validation
```

In the TUI:

| Key | Action |
|---|---|
| `h` | Toggle hint |
| `r` | Reset current exercise |
| `n` | Skip success animation |
| `l` | Toggle exercise list |
| `q` | Quit |

## How an exercise works

Each file in `exercises/` contains:
1. A `# I AM NOT DONE` line near the top (the gate).
2. Broken code you have to fix.
3. A block of `assert` statements at the bottom (the checks — don't edit).

When the script exits 0 *and* you've removed `# I AM NOT DONE`, pylings advances you to the next exercise.

## Adding exercises

1. Create the file under `exercises/<topic>/<name>.py` with the marker, the broken code, and the asserts.
2. Add an entry to `info.toml`, including a `hint`.
3. The curriculum order is the order in `info.toml`.

## Development

```bash
pip install -e ".[dev]"
pytest                                                  # all tests
pylings --root tests/fixtures/passing_curriculum verify  # smoke-check the runner
```