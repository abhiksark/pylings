# Pylings — Roadmap Curriculum Completion Design

**Date:** 2026-05-23
**Status:** Approved for implementation
**Owner:** abhiksark@gmail.com
**Builds on:** `2026-05-20-pylings-topics-and-curriculum-design.md`

## Goal

Complete the planned 31-topic curriculum by adding the seven specialized topics that are still missing from `info.toml`, `exercises/`, and `checks/`.

Current state:

- 234 exercises
- 24 topics
- Matching exercise/check file count

Target state:

- 292 exercises
- 31 topics
- Matching exercise/check file count

## Topics To Add

| Topic | Count | Covers |
|---|---:|---|
| `itertools` | 8 | `chain`, `islice`, `product`, `groupby`, `accumulate`, `cycle`, `zip_longest`, composition |
| `json` | 8 | `loads`, `dumps`, nested data, defaults, round-tripping, file-like workflows |
| `datetime` | 8 | `date`, `datetime`, `timedelta`, parsing, formatting, comparison |
| `enums` | 6 | `Enum`, `auto`, values, iteration, comparisons, behavior methods |
| `pathlib` | 6 | `Path`, joining, suffixes, parents, glob-like filtering, reading/writing paths |
| `oop_advanced` | 12 | inheritance, `super`, polymorphism, properties, dunder methods, ABCs, mixins |
| `async` | 10 | `async def`, `await`, `asyncio.run`, `gather`, tasks, cancellation-aware patterns |

## Exercise Format

Each new exercise follows the existing hidden-check model:

- `exercises/<topic>/<topic><N>.py` contains:
  - `# Exercise: <Readable Topic> <N>`
  - `# I AM NOT DONE`
  - a concise goal comment
  - intentionally broken beginner-facing code
- `checks/<topic>/<topic><N>.py` contains hidden assertions and a short pass print.
- `info.toml` contains one matching `[[exercises]]` entry with a useful hint.

Exercise names remain globally unique.

## Difficulty Ramp

Within each topic:

- Exercises 1-3 introduce one concept with small fill-in fixes.
- Exercises 4-7 apply the concept in a short function or transformation.
- Final exercises combine two or more ideas from the topic.

Each broken file should be solvable in a few lines. Goal comments must state the expected behavior without requiring learners to inspect hidden checks.

## Ordering

Append the seven new topics after `collections`, preserving the roadmap order:

1. `itertools`
2. `json`
3. `datetime`
4. `enums`
5. `pathlib`
6. `oop_advanced`
7. `async`

This keeps the existing curriculum order stable.

## Verification

Add a unit test that loads the real repository curriculum and asserts:

- total exercise count is 292
- topic count is 31
- each planned new topic has the expected number of exercises
- each manifest entry has an existing exercise file and check file, via the existing manifest loader

Run:

- `.venv/bin/python -m pytest -q`

`pylings verify` is not a gate for the real curriculum because exercises are intentionally broken for learners.
