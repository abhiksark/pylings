# Local Docs

Pylings bundles short Python reference snippets so learners can stay in the
terminal while solving exercises.

## In The TUI

- Press `F5` to open the local docs window for the current exercise.
- Press `O` from the docs window to open the official Python docs page.
- Press `Esc` to close the docs window and return to the exercise.

## Source Material

Bundled snippets are generated from the official Python documentation. Licensing
details live in `pylings/docs/NOTICE.md`.

## Refresh Snippets

Run this from the repository root:

```bash
python scripts/fetch_python_docs.py
```

The generated files live under:

```text
pylings/docs/index.json
pylings/docs/topics/
```

When adding or changing exercises, keep `info.toml` docs links aligned with the
local topic snippets.
