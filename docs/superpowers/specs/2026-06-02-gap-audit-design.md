# Pylings Gap-Audit — Design Spec

- **Date:** 2026-06-02
- **Status:** Approved for planning
- **Scope:** Curriculum gaps + Product/feature gaps
- **Approach:** Hybrid (C) — quantified curriculum, checklist product

## Goal

Build a **reusable gap-audit playbook** and **run it once** to produce a first
gap-analysis report. The audit covers two domains:

1. **Curriculum gaps** — judged against (a) *popular learning paths* (what
   courses, bootcamps, and working Python devs actually cover) and (b)
   *internal consistency* (per-topic counts, difficulty curve, concept
   coverage, dead spots).
2. **Product/feature gaps** — what a learner can't do yet, judged against
   *Rustlings* (pylings is explicitly Rustlings-style) plus common TUI
   learning-tool UX conventions.

Explicitly **out of scope**: code-quality/test gaps and adoption/growth gaps.

## Deliverables

| Artifact | Purpose | Re-run cadence |
|---|---|---|
| `scripts/curriculum_audit.py` | Instrumentation: extracts the coverage/difficulty matrix and computes curriculum gaps. Stdlib-only, no new dependencies. | Every release |
| `docs/refs/expected-concepts.toml` | Versioned external baseline: per-topic expected concepts with detection hints. | Edited as the baseline evolves |
| `docs/gap-audit-playbook.md` | The reusable methodology: how to run the script, update the baseline, the internal-consistency rules, the product checklist template, and the scoring rubric. | Read each audit |
| `docs/gap-analysis-2026-06.md` | The first run's findings. | One per audit, dated |

## Part 1 — Curriculum (quantified, re-runnable)

### 1a. Extraction (`scripts/curriculum_audit.py`)

Walks `exercises/`, `checks/`, `solutions/_answers.py`, and `info.toml`.
Per exercise it captures:

- **Identity:** topic, exercise name, order index (from `info.toml`).
- **Goal text:** the leading `# ...` header comment block.
- **Difficulty signals:** exercise LOC (excluding comments), `???`-blank count,
  check LOC, reference-answer LOC.

Emits a **coverage matrix** in two formats:
- `docs/refs/coverage-matrix.json` (machine-readable, for diffing across runs)
- A markdown table embedded in the report.

### 1b. Expected-concepts reference (`docs/refs/expected-concepts.toml`)

Hand-built, versioned, per-topic list of concepts a popular-learning-path
curriculum would cover. Each concept carries **detection hints** (keywords / API
names / operators). Example:

```toml
[strings]
f_string_format = { hints = [":>", ":.2f", "!r"] }
walrus          = { hints = [":="] }

[functions]
keyword_only_args = { hints = ["*,"] }
```

Sourced from common courses/bootcamps (e.g. RealPython-style tracks) and
job-relevance, not from exhaustive language coverage.

### 1c. Gap computation (in-script)

- **Coverage gaps:** for each expected concept, scan the combined
  exercise + reference-answer text of that topic for any detection hint. No hint
  found → `MISSING` gap. (Concept detection method: **keyword/API scan**, see
  "Concept detection" below.)
- **Internal-consistency flags** (no external baseline needed):
  - *Count variance:* topics whose exercise count deviates sharply from the
    median (flag low and high outliers).
  - *Difficulty-curve anomalies:* within a topic, exercises ordered such that a
    high-difficulty-signal exercise appears early, or the curve is flat, or
    there's a large jump between adjacent exercises.
  - *Ordering smells:* concepts whose detection hint first appears in a later
    topic than where it's conceptually prerequisite (best-effort heuristic).

### Concept detection method (decided)

**Keyword/API scan now; explicit tags deferred.** v1 uses the detection hints in
`expected-concepts.toml` to scan exercise+answer text — zero curriculum changes,
fully automated, accepted as slightly fuzzy. The playbook documents that if
false positives/negatives prove material, explicit `# concepts: a, b` lines can
be added per topic incrementally later. The 292-file tagging cost is **not** paid
in this audit.

## Part 2 — Product/feature (structured checklist)

A capability checklist organized by area:

- Onboarding / install
- Navigation (move between exercises/topics, jump, search)
- Feedback loop (watch mode, verify, re-run on save)
- Hints (presence, escalation levels)
- Progress / state (resume, completion %, streak)
- Help / docs (in-app docs, keybinding help)
- Accessibility (color, screen-reader, no-color/CI mode)
- Configurability (paths, theme, editor integration)

Each item is scored **present / partial / missing**, with the baseline
reference (Rustlings has it, or a UX convention) and a note. First run: read
`pylings/cli.py`, `pylings/app.py`, `pylings/screens/`, `pylings/widgets/`,
compare to Rustlings' feature set, and fill the checklist.

## Part 3 — Report format (`docs/gap-analysis-2026-06.md`)

1. **Summary** — headline counts and the top findings.
2. **Curriculum gaps** — missing-concept table (topic × concept × severity ×
   effort) followed by internal-consistency findings.
3. **Product gaps** — the filled checklist, then prioritized findings.
4. **Ranked candidate shortlist for v0.3** — top findings across both domains,
   ranked. This is a *candidate* list to inform a roadmap, **not** a commitment.

**Scoring rubric (applied to every finding):**
- **Severity:** High (core skill / common learner blocker) · Medium · Low
  (nice-to-have / rare).
- **Effort:** S (≤1 day / few exercises) · M · L (multi-day / new subsystem).

## Playbook contents (`docs/gap-audit-playbook.md`)

- How to run `scripts/curriculum_audit.py` and read its output.
- How to update `expected-concepts.toml` as the baseline evolves.
- The internal-consistency rules and their thresholds.
- The blank product capability checklist (copy per audit).
- The severity/effort rubric and how to write the dated report.
- Cadence: run each release; diff `coverage-matrix.json` against the prior run
  to catch regressions.

## Components and boundaries

- `curriculum_audit.py` is a self-contained CLI: input = repo curriculum dirs +
  `expected-concepts.toml`; output = `coverage-matrix.json` + a printed markdown
  report fragment. It performs **no** writes to curriculum files. Testable in
  isolation against `tests/fixtures/` curricula.
- The reference (`expected-concepts.toml`) and the report are **data/docs**, not
  code — they change without touching the script.
- The product checklist is a human process documented in the playbook; it has no
  code dependency on the script.

## Non-goals

- No changes to curriculum exercise files in this audit (tagging deferred).
- No new runtime dependencies; script is stdlib-only.
- No automated product-gap scoring (kept qualitative on purpose).
- The report ranks candidates; it does not decide or implement the v0.3 roadmap.
