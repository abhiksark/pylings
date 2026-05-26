# Pylings Docs Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and deploy a static documentation site for Pylings at `https://pylings.abhik.ai/`.

**Architecture:** Add a repository-native MkDocs site under `docs-site/`, with existing README/demo content reorganized into focused documentation pages. Deploy the generated static site to GitHub Pages using GitHub Actions, with `pylings.abhik.ai` configured as the custom domain.

**Tech Stack:** MkDocs, MkDocs Material, Markdown, GitHub Actions Pages, existing GIF and PNG assets under `docs/assets/`.

---

## Scope Check

This plan covers one subsystem: the public documentation site and its deployment workflow. It does not change the terminal app, curriculum runtime, PyPI publishing, or the `v0.1.0` release tag.

## File Structure

- Create `requirements-docs.txt`: documentation build dependency entry point.
- Create `mkdocs.yml`: MkDocs configuration, navigation, theme, canonical site URL, repository links, and search.
- Create `docs-site/index.md`: docs homepage with product overview and demo GIF.
- Create `docs-site/quick-start.md`: install, workspace setup, and command guide.
- Create `docs-site/interface.md`: TUI screenshots and key binding reference.
- Create `docs-site/curriculum.md`: topic list, exercise model, hidden checks, and progress behavior.
- Create `docs-site/local-docs.md`: bundled Python docs behavior and regeneration command.
- Create `docs-site/contributing.md`: contributor workflow and repository conventions.
- Create `docs-site/roadmap.md`: v0.1.0 status and next hardening work.
- Create `docs-site/CNAME`: GitHub Pages custom domain.
- Create `docs-site/robots.txt`: crawler policy and sitemap reference.
- Create `.github/workflows/pages.yml`: GitHub Pages build and deploy workflow.
- Modify `Readme.md`: add a clear documentation-site link near the top.
- Modify `pyproject.toml`: point `Documentation` metadata to `https://pylings.abhik.ai/`.

## Task 1: Minimal MkDocs Scaffold

**Files:**
- Create: `requirements-docs.txt`
- Create: `mkdocs.yml`
- Create: `docs-site/index.md`

- [ ] **Step 1: Confirm there is no docs-site scaffold**

Run:

```bash
test ! -f mkdocs.yml && test ! -d docs-site && echo "docs site scaffold missing"
```

Expected:

```text
docs site scaffold missing
```

- [ ] **Step 2: Create `requirements-docs.txt`**

Create the file with:

```text
mkdocs-material>=9.5
```

- [ ] **Step 3: Create initial `mkdocs.yml`**

Create the file with:

```yaml
site_name: Pylings
site_url: https://pylings.abhik.ai/
site_description: Python learnings, Rustlings-style, in a terminal TUI.
repo_url: https://github.com/abhiksark/pylings
repo_name: abhiksark/pylings
edit_uri: edit/main/docs-site/
docs_dir: docs-site

theme:
  name: material
  language: en
  features:
    - navigation.sections
    - navigation.top
    - search.highlight
    - search.suggest
    - content.code.copy
  palette:
    - scheme: default
      primary: blue
      accent: amber

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences

plugins:
  - search

nav:
  - Home: index.md

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/abhiksark/pylings
```

- [ ] **Step 4: Create `docs-site/index.md`**

Create the file with:

````markdown
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
````

- [ ] **Step 5: Install docs dependencies**

Run:

```bash
python -m pip install -r requirements-docs.txt
```

Expected: exit code 0.

- [ ] **Step 6: Build the minimal site**

Run:

```bash
mkdocs build --strict
```

Expected: exit code 0 and output containing:

```text
Documentation built
```

- [ ] **Step 7: Commit the scaffold**

Run:

```bash
git add requirements-docs.txt mkdocs.yml docs-site/index.md
git commit -m "docs: add mkdocs scaffold"
```

## Task 2: Full Documentation Content

**Files:**
- Modify: `mkdocs.yml`
- Create: `docs-site/quick-start.md`
- Create: `docs-site/interface.md`
- Create: `docs-site/curriculum.md`
- Create: `docs-site/local-docs.md`
- Create: `docs-site/contributing.md`
- Create: `docs-site/roadmap.md`

- [ ] **Step 1: Expand navigation in `mkdocs.yml`**

Replace the `nav:` block with:

```yaml
nav:
  - Home: index.md
  - Quick Start: quick-start.md
  - Interface: interface.md
  - Curriculum: curriculum.md
  - Local Docs: local-docs.md
  - Contributing: contributing.md
  - Roadmap: roadmap.md
```

- [ ] **Step 2: Verify missing pages fail the strict build**

Run:

```bash
mkdocs build --strict
```

Expected: exit code 1 with output mentioning missing files such as `quick-start.md`.

- [ ] **Step 3: Create `docs-site/quick-start.md`**

Create the file with:

````markdown
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

`pylings init` copies exercises, hidden checks, local docs, and reset snapshots
into a learner workspace. Run `pylings` from that workspace to open the first
pending exercise.

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
````

- [ ] **Step 4: Create `docs-site/interface.md`**

Create the file with:

````markdown
# Interface

## Coding Screen

![Coding screen](https://raw.githubusercontent.com/abhiksark/pylings/main/docs/assets/screenshots/coding-screen.png)

The coding screen keeps the exercise, editor, output, progress, and exercise
list in one terminal view. Checks rerun as files change.

## Topic Picker

![Topic picker](https://raw.githubusercontent.com/abhiksark/pylings/main/docs/assets/screenshots/topic-picker.png)

The topic picker shows curriculum progress by topic and lets learners jump back
to a topic without leaving the terminal.

## Local Docs Window

![Local docs reference](https://raw.githubusercontent.com/abhiksark/pylings/main/docs/assets/screenshots/docs-reference.png)

The docs window opens bundled Python reference snippets for the current
exercise. Press `O` from that window to open the official Python docs page.

## Key Bindings

| Key | Action |
|---|---|
| `F1` | Toggle hint |
| `F2` | Reset the current exercise |
| `F3` | Toggle the exercise list |
| `F4` | Return to the topic picker |
| `F5` | Show the local Python reference |
| `O` | Open official docs from the reference window |
| `Esc` | Close docs, or quit from main screens |
| `Ctrl+Q` | Quit |
````

- [ ] **Step 5: Create `docs-site/curriculum.md`**

Create the file with:

````markdown
# Curriculum

Pylings ships 292 exercises across 31 topics. Each exercise has a learner file,
a hidden check file, a hint, and a Python documentation link in `info.toml`.

## Topic Coverage

| Topic | Exercises |
|---|---:|
| `variables` | 10 |
| `strings` | 10 |
| `conditionals` | 10 |
| `loops` | 10 |
| `functions` | 10 |
| `lists` | 10 |
| `tuples` | 10 |
| `dictionaries` | 10 |
| `sets` | 10 |
| `comprehensions` | 10 |
| `exceptions` | 10 |
| `file_io` | 10 |
| `classes` | 12 |
| `functional` | 10 |
| `decorators` | 10 |
| `generators` | 10 |
| `context_managers` | 8 |
| `dataclasses` | 8 |
| `type_hints` | 8 |
| `regex` | 10 |
| `testing` | 12 |
| `recursion` | 8 |
| `modules` | 8 |
| `collections` | 10 |
| `itertools` | 8 |
| `json` | 8 |
| `datetime` | 8 |
| `enums` | 6 |
| `pathlib` | 6 |
| `oop_advanced` | 12 |
| `async` | 10 |

## File Model

```text
exercises/<topic>/<exercise>.py   # learner-editable code
checks/<topic>/<exercise>.py      # hidden assertions
solutions/<exercise>.py           # reference answer
info.toml                         # order, hints, docs links
```

Exercise and check filenames stay mirrored. For example,
`exercises/lists/lists3.py` is checked by `checks/lists/lists3.py`.

## Progress

Progress is stored in the learner workspace, not in the package repository.
Passing checks mark exercises complete. Reset restores a learner file from the
original snapshot created during `pylings init`.
````

- [ ] **Step 6: Create `docs-site/local-docs.md`**

Create the file with:

````markdown
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
````

- [ ] **Step 7: Create `docs-site/contributing.md`**

Create the file with:

````markdown
# Contributing

Read `AGENTS.md` for repository conventions and `CONTRIBUTING.md` for the
contributor workflow.

## Development Setup

```bash
git clone git@github.com:abhiksark/pylings.git
cd pylings
pip install -e ".[dev]"
python -m pytest -q
```

## Test Commands

```bash
python -m pytest -q
pylings --root tests/fixtures/passing_curriculum verify
python -m build
```

Use unit tests for core behavior, integration tests for CLI and workspace flows,
and TUI tests for Textual keyboard interactions.

## Curriculum Changes

Update these together:

```text
exercises/<topic>/<exercise>.py
checks/<topic>/<exercise>.py
solutions/<exercise>.py
info.toml
```

Keep exercise names stable and mirrored. Use topic-plus-number names such as
`variables1.py`, `collections10.py`, and `oop_advanced12.py`.
````

- [ ] **Step 8: Create `docs-site/roadmap.md`**

Create the file with:

````markdown
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
````

- [ ] **Step 9: Build the full docs site**

Run:

```bash
mkdocs build --strict
```

Expected: exit code 0 and output containing:

```text
Documentation built
```

- [ ] **Step 10: Commit the content pages**

Run:

```bash
git add mkdocs.yml docs-site/quick-start.md docs-site/interface.md docs-site/curriculum.md docs-site/local-docs.md docs-site/contributing.md docs-site/roadmap.md
git commit -m "docs: add docs site content"
```

## Task 3: Domain And Discovery Files

**Files:**
- Create: `docs-site/CNAME`
- Create: `docs-site/robots.txt`

- [ ] **Step 1: Create `docs-site/CNAME`**

Create the file with:

```text
pylings.abhik.ai
```

- [ ] **Step 2: Create `docs-site/robots.txt`**

Create the file with:

```text
User-agent: *
Allow: /

Sitemap: https://pylings.abhik.ai/sitemap.xml
```

- [ ] **Step 3: Verify MkDocs includes the files**

Run:

```bash
mkdocs build --strict
test "$(cat site/CNAME)" = "pylings.abhik.ai"
grep -F "Sitemap: https://pylings.abhik.ai/sitemap.xml" site/robots.txt
```

Expected:

```text
Sitemap: https://pylings.abhik.ai/sitemap.xml
```

- [ ] **Step 4: Commit domain files**

Run:

```bash
git add docs-site/CNAME docs-site/robots.txt
git commit -m "docs: add pages custom domain files"
```

## Task 4: GitHub Pages Workflow

**Files:**
- Create: `.github/workflows/pages.yml`

- [ ] **Step 1: Confirm Pages workflow is absent**

Run:

```bash
test ! -f .github/workflows/pages.yml && echo "pages workflow missing"
```

Expected:

```text
pages workflow missing
```

- [ ] **Step 2: Create `.github/workflows/pages.yml`**

Create the file with:

```yaml
name: pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: pip
          cache-dependency-path: requirements-docs.txt
      - uses: actions/configure-pages@v5
      - run: python -m pip install -r requirements-docs.txt
      - run: mkdocs build --strict
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 3: Verify workflow text and docs build**

Run:

```bash
python - <<'PY'
from pathlib import Path

workflow = Path(".github/workflows/pages.yml").read_text(encoding="utf-8")
required = [
    "actions/configure-pages@v5",
    "actions/upload-pages-artifact@v3",
    "actions/deploy-pages@v4",
    "mkdocs build --strict",
]
missing = [item for item in required if item not in workflow]
if missing:
    raise SystemExit(f"missing workflow entries: {missing}")
print("pages workflow entries present")
PY
mkdocs build --strict
```

Expected:

```text
pages workflow entries present
```

The `mkdocs build --strict` command should exit 0.

- [ ] **Step 4: Commit the workflow**

Run:

```bash
git add .github/workflows/pages.yml
git commit -m "ci: deploy docs with github pages"
```

## Task 5: Repository Links And Package Metadata

**Files:**
- Modify: `Readme.md`
- Modify: `pyproject.toml`

- [ ] **Step 1: Update README discovery links**

In `Readme.md`, add this line after the badge block and before the short
description:

```markdown
Documentation: [pylings.abhik.ai](https://pylings.abhik.ai/)
```

- [ ] **Step 2: Update package documentation URL**

In `pyproject.toml`, change:

```toml
Documentation = "https://github.com/abhiksark/pylings#readme"
```

to:

```toml
Documentation = "https://pylings.abhik.ai/"
```

- [ ] **Step 3: Verify metadata parses**

Run:

```bash
python - <<'PY'
from pathlib import Path
import tomllib

data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
url = data["project"]["urls"]["Documentation"]
assert url == "https://pylings.abhik.ai/", url
print(url)
PY
```

Expected:

```text
https://pylings.abhik.ai/
```

- [ ] **Step 4: Build package metadata**

Run:

```bash
python -m pip install build
python -m build
```

Expected: exit code 0 with wheel and source distribution written under `dist/`.

- [ ] **Step 5: Commit repository link updates**

Run:

```bash
git add Readme.md pyproject.toml
git commit -m "docs: link public documentation site"
```

## Task 6: Final Verification And Push

**Files:**
- Verify: entire working tree

- [ ] **Step 1: Run docs verification**

Run:

```bash
mkdocs build --strict
git diff --check
```

Expected: both commands exit 0.

- [ ] **Step 2: Run focused package verification**

Run:

```bash
python -m pytest -q
pylings --root tests/fixtures/passing_curriculum verify
```

Expected: both commands exit 0.

- [ ] **Step 3: Inspect final diff**

Run:

```bash
git status --short --branch
git log --oneline -6
```

Expected: branch is ahead of `origin/main` by the new docs commits and has no
unstaged changes.

- [ ] **Step 4: Push to GitHub**

Run:

```bash
git push origin main
```

Expected: push succeeds and the `pages` workflow starts on GitHub.

- [ ] **Step 5: Manual GitHub Pages settings**

In the repository UI, set:

```text
Settings -> Pages -> Source: GitHub Actions
Settings -> Pages -> Custom domain: pylings.abhik.ai
```

In Vercel DNS for `abhik.ai`, set:

```text
Type: CNAME
Name: pylings
Value: abhiksark.github.io
```

- [ ] **Step 6: Verify deployed domain**

After DNS and Pages finish provisioning, run:

```bash
dig +short pylings.abhik.ai CNAME
curl -I https://pylings.abhik.ai/
```

Expected DNS output:

```text
abhiksark.github.io.
```

Expected curl headers include:

```text
HTTP/2 200
server: GitHub.com
```

## Self-Review

- Spec coverage: Tasks 1 and 2 build the MkDocs site and required pages. Task 3 covers domain, crawler, and custom domain files. Task 4 covers GitHub Actions deployment. Task 5 covers repository/package discovery links. Task 6 covers local verification, push, manual DNS/Page settings, and deployed-domain checks.
- Placeholder scan: The plan uses exact file paths, concrete file content, exact commands, and expected outcomes.
- Type and name consistency: The plan uses `docs-site/` as `docs_dir`, `site/` as the MkDocs output directory, `pylings.abhik.ai` as the custom domain, and `requirements-docs.txt` as the workflow dependency file throughout.
