# Pylings Docs Site Design

**Date:** 2026-05-26
**Status:** Draft for review
**Owner:** abhiksark@gmail.com

## Goal

Create a proper documentation site for Pylings at `https://pylings.abhik.ai/`.
The site should make the project easier to discover, explain the learner flow
better than a single README can, and provide a stable place for screenshots,
demo media, install instructions, curriculum details, and contributor guidance.

## Current State

The project has a strong README, a generated terminal demo GIF, screenshots, and
local Python documentation snippets. GitHub Pages is not yet configured for this
repository, and the default `abhiksark.github.io/pylings/` path is not useful
because the user site redirects to the personal domain. A custom Pages domain is
therefore the right path.

## Target Site

Use a static MkDocs site deployed by GitHub Actions. The site remains lightweight
and repository-native: Markdown content, no backend, no JavaScript application,
and no duplicated product logic.

Primary pages:

- `Home`: product summary, demo GIF, key capabilities, install entry point.
- `Quick Start`: install from GitHub tag, initialize workspace, run the TUI, use
  common CLI commands.
- `Interface`: screenshots and key bindings for coding, topic picker, docs
  window, hints, reset, and quit behavior.
- `Curriculum`: topic list, exercise/check model, hidden checks, docs links, and
  how progress works.
- `Local Docs`: how bundled Python docs are generated, how `F5` and `O` behave,
  and how to refresh snippets with `scripts/fetch_python_docs.py`.
- `Contributing`: links to `AGENTS.md`, `CONTRIBUTING.md`, test commands, and
  the mirrored `exercises/<topic>/` plus `checks/<topic>/` convention.
- `Roadmap`: v0.1.0 alpha status, PyPI publishing status, and the next product
  hardening areas.

## Domain And Deployment

GitHub Pages should serve the custom domain `pylings.abhik.ai`. DNS should be:

```text
Type: CNAME
Name: pylings
Value: abhiksark.github.io
```

GitHub repository settings should use:

```text
Settings -> Pages -> Source: GitHub Actions
Settings -> Pages -> Custom domain: pylings.abhik.ai
```

The repository should include a Pages workflow that builds the static site on
pushes to `main` and on manual dispatch.

## Assets

The docs site should reuse the existing media:

- `docs/assets/demos/pylings-demo.gif`
- `docs/assets/screenshots/coding-screen.png`
- `docs/assets/screenshots/topic-picker.png`
- `docs/assets/screenshots/docs-reference.png`

To avoid copying large binaries, Markdown pages can reference the repository
assets through stable raw GitHub URLs. If that becomes brittle later, add an
asset-copy step to the docs build.

## SEO And Discovery

Use a clear `site_name`, `site_description`, canonical `site_url`, repo links,
and readable page titles. The home page should include search-friendly language:
Python learnings, Rustlings-style Python exercises, terminal TUI, beginner
Python practice, hidden checks, local Python docs, and self-paced coding
practice.

## Testing

The implementation must pass:

- `mkdocs build --strict`
- `git diff --check`

The workflow should fail if internal links, nav entries, or Markdown references
are broken. No application test suite is required for a docs-only change unless
package metadata or runtime code changes.

## Non-Goals

- Do not build a separate web app.
- Do not move the learner experience out of the terminal.
- Do not publish PyPI as part of this change.
- Do not change the v0.1.0 release tag.

## Acceptance Criteria

- A local `mkdocs build --strict` produces a complete static site.
- GitHub Actions can deploy the site to GitHub Pages.
- The site explains install, first run, interface, curriculum, local docs, and
  contribution flow without requiring users to read the whole README first.
- The custom domain instructions are documented clearly enough for manual DNS
  setup in Vercel.
