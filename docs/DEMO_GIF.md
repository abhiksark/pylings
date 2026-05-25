# Demo GIF Workflow

Use this workflow to generate a repeatable GIF for the README, GitHub release,
and PyPI project page. The goal is to show the real `pylings` first-run flow,
not a mocked terminal.

## Recommended Tool

Use [VHS](https://github.com/charmbracelet/vhs). It records scripted terminal
sessions and produces a GIF without manual screen capture.

```bash
brew install charmbracelet/tap/vhs
```

## Generate the GIF

From the repository root:

```bash
pip install -e ".[dev]"
scripts/generate_demo_gif.sh
```

To use a specific VHS binary, set `VHS_BIN`:

```bash
VHS_BIN=/path/to/vhs scripts/generate_demo_gif.sh
```

If Homebrew VHS fails on macOS with `could not open ttyd` and
`ERR_CONNECTION_REFUSED`, use a newer VHS build or run VHS through Docker. That
failure happens before Pylings starts.

The tape writes:

```text
docs/assets/demos/pylings-demo.gif
```

Review the GIF before committing it. Keep the recording under 20 seconds so it
loads quickly on GitHub and PyPI.

## What the Demo Shows

The scripted flow should stay focused on the first-time user path:

1. Initialize a clean workspace.
2. Open the Pylings TUI.
3. Show the first pending exercise in the coding screen.
4. Open local docs with `F5` if the recording is stable.
5. Quit with `Esc` or `Ctrl+Q`.

## Fallback Workflow

If VHS cannot control the TUI reliably on a machine, record an asciinema cast
and render it with `agg`:

```bash
brew install asciinema agg
asciinema rec docs/assets/demos/pylings.cast
agg docs/assets/demos/pylings.cast docs/assets/demos/pylings-demo.gif
```

The VHS path is preferred because `docs/demo.tape` keeps the public demo
repeatable across releases.
