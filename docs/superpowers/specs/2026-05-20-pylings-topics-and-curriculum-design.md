# Pylings — Topic Tracks & Curriculum Expansion Design

**Date:** 2026-05-20
**Status:** Design approved, pending implementation plan
**Owner:** abhiksark@gmail.com
**Builds on:** `2026-05-19-pylings-rustlings-ux-design.md`, `2026-05-20-pylings-builtin-editor-design.md`, `2026-05-20-pylings-hidden-checks-design.md`

## Goal

Two things in one cycle:

1. **Topic tracks** — turn pylings from a single linear curriculum into a set of independent per-topic tracks. The learner picks a topic ("I want to practice loops") and works through that topic's exercises in order; topics don't gate each other; progress is tracked per topic.
2. **A large curriculum** — grow the curriculum from 3 exercises to **31 topics, ≈300 exercises**, spanning beginner, advanced, and specialized Python.

## Why this matters

A 3-exercise linear curriculum is a proof of concept, not a learning tool. Learners want to practice what they choose, and they want depth. Per-topic tracks give them agency; a 300-exercise curriculum gives them somewhere to go.

## Non-goals

- A repo-wide `solutions/` tree for end-to-end CI verification of the real curriculum (noted as a deferred follow-up — it would double the content).
- Cross-topic prerequisites or unlock rules. Every topic is open from the start.
- Spelling out all ~300 exercises in this spec. The spec fixes the topic inventory, the exercise template, and the difficulty rubric; the exercises themselves are authored during implementation, one topic per task.
- Changing the exercise/check file format, the runner, or the `# I AM NOT DONE` marker. Within a topic, progression is still strictly linear and marker-gated exactly as today.

---

## Decisions locked in during brainstorming

| Topic | Decision |
|---|---|
| Topic model | Per-topic tracks — each topic an independent linear sequence |
| Topic definition | Derived from the exercise path's directory; no `info.toml` format change |
| State model | Flat `completed` set; the global `current` cursor is removed; `format_version` → 2 |
| TUI entry | A topic-picker screen; selecting a topic enters its track screen |
| CLI | `list` / `list <topic>` / `start <topic>` / `verify [<topic>]` |
| Curriculum | 31 topics, ≈300 exercises, in three tiers (core / advanced / specialized) |
| Build shape | Feature first (Phase 1), then one task per topic (Phase 2) |

---

## The per-topic model

### Topics are derived, not declared

`info.toml` stays a flat `[[exercises]]` array. A topic is the directory component of an exercise's path: `exercises/loops/loops3.py` belongs to topic `loops`. The manifest groups exercises by topic.

- **Topic order** = order of first appearance in `info.toml`.
- **Exercise order within a topic** = `info.toml` order.

New `Manifest` helpers (no format change):

```python
def topics(self) -> list[str]:
    """Topic names in first-appearance order."""

def exercises_in(self, topic: str) -> list[Exercise]:
    """Exercises of one topic, in curriculum order."""
```

### State model

Per-topic tracks remove the need for a single global cursor. `state.json` keeps only the completed set:

```json
{ "format_version": 2, "completed": ["variables1", "loops3", "loops4"] }
```

- Exercise names are globally unique (the manifest enforces this), so a flat set suffices.
- Everything per-topic is **derived**: a topic's progress is `len([e for e in exercises_in(topic) if e.name in completed])` of its total; a topic's "current" exercise is the first one not in `completed`.
- `format_version` bumps to `2`. An old v1 file fails the existing `format_version` check in `State.load` and trips the corruption-recovery path (backed up to `.bak`, fresh state returned). `.pylings/state.json` is gitignored local progress, so discarding it is acceptable — no migration code.

`State` becomes simpler:

```python
@dataclass
class State:
    completed: set[str] = field(default_factory=set)

    def mark_done(self, name: str) -> None:
        self.completed.add(name)
```

The global-`current` rewind logic in `pylings reset` is removed — `reset` becomes "remove the name from `completed`, restore the file from its snapshot."

### Unchanged

The runner, the `checks/` tree, the `# I AM NOT DONE` marker, per-exercise verification, and within-topic linear gating are all unchanged. The change is: global ordering becomes per-topic ordering, plus a topic-selection layer.

---

## TUI: topic picker & track screens

The TUI becomes two Textual `Screen`s.

### Topic picker screen (the entry point)

```
┌─ pylings ─ topics ──────────────────────┐
│   variables       10/10  ✓              │
│   strings          3/10  ●              │
│   loops            0/10                 │
│   …                                     │
└─ ↑↓ select · enter open · ^Q quit ──────┘
```

- A list of every topic with `done/total` progress and a status marker: ✓ complete, ● started, (blank) untouched.
- `↑`/`↓` move, `Enter` opens the highlighted topic's track. `Ctrl+Q` quits.

### Track screen (one topic)

The existing editor + output + exercise-tree layout from the built-in-editor design, **scoped to the selected topic**:

- The `F3` exercise tree lists only this topic's exercises.
- The editor opens on the topic's current (first uncompleted) exercise.
- Within the topic, the auto-save → run → advance loop is exactly as today.
- Finishing the topic's last exercise shows a brief "topic complete" state, then returns to the picker (the topic now shows ✓).

### Bindings

`F1` hint · `F2` reset · `F3` exercise list · **`F4` topics (back to the picker)** · `Ctrl+Q` quit. `F1`–`F3` and `Ctrl+Q` are unchanged from the built-in-editor design; `F4` is new.

### Flow

```
pylings ──► topic picker ──(pick)──► track screen for that topic
                 ▲                          │
                 └────── F4, or topic ───────┘
                         complete
```

`pylings` (no args) always opens the picker. The TUI session holds the selected topic in memory; it is not persisted (the picker is always the entry point).

---

## CLI

| Command | Behavior |
|---|---|
| `pylings` / `pylings watch` | Launch the TUI; open the topic picker |
| `pylings start <topic>` | Launch the TUI; jump straight into that topic's track |
| `pylings list` | List every topic with `done/total` progress |
| `pylings list <topic>` | List that topic's exercises with ✓/●/🔒 markers |
| `pylings run <name>` | Run one exercise (unchanged — names are globally unique) |
| `pylings hint <name>` | Print an exercise's hint (unchanged) |
| `pylings reset <name> [--yes]` | Restore an exercise; remove it from `completed` (unchanged behavior, minus the global-cursor rewind) |
| `pylings verify [<topic>]` | Run the whole curriculum (CI), or just one topic (curriculum-author check) |

Unknown topic names in `start` / `list` / `verify` fail fast with a clear error that lists the valid topics. The lazy-import discipline holds — only `watch` / `start` / no-arg import Textual.

---

## The curriculum — 31 topics, ≈300 exercises

Three tiers, in this order (the picker presents them in this order):

### Core tier (13 topics, ≈133 exercises)

| Topic | Count | Topic | Count |
|---|---|---|---|
| `variables` | 10 | `tuples` | 10 |
| `strings` | 10 | `dictionaries` | 10 |
| `conditionals` | 10 | `sets` | 10 |
| `loops` | 10 | `comprehensions` | 10 |
| `functions` | 10 | `exceptions` | 10 |
| `lists` | 10 | `file_io` | 10 |
| | | `classes` | 13 |

### Advanced tier (8 topics, ≈76 exercises)

| Topic | Count | Covers |
|---|---|---|
| `functional` | 10 | `lambda`, `map`/`filter`, higher-order functions |
| `decorators` | 10 | wrapping functions, `functools.wraps`, arguments |
| `generators` | 10 | `yield`, generator expressions, iterators, `__iter__` |
| `context_managers` | 8 | `with`, `__enter__`/`__exit__`, `contextlib` |
| `dataclasses` | 8 | `@dataclass`, fields, defaults, `frozen` |
| `type_hints` | 8 | annotations, `list[int]`, `Optional`, `Protocol` |
| `regex` | 10 | `re.match`/`search`/`findall`, groups, substitution |
| `testing` | 12 | `assert`, `pytest` test functions, `pytest.raises`, `parametrize`, fixtures |

### Specialized tier (10 topics, ≈84 exercises)

| Topic | Count | Covers |
|---|---|---|
| `recursion` | 8 | base/recursive cases, tree and accumulator patterns |
| `modules` | 8 | `import`, packages, `__name__`, `__main__` |
| `collections` | 10 | `Counter`, `defaultdict`, `namedtuple`, `deque` |
| `itertools` | 8 | `chain`, `groupby`, `product`, `accumulate` |
| `json` | 8 | `loads`/`dumps`, nested data, round-tripping |
| `datetime` | 8 | `date`, `datetime`, `timedelta`, formatting |
| `enums` | 6 | `Enum`, members, `auto()`, iteration |
| `pathlib` | 6 | `Path`, joining, globbing, reading |
| `oop_advanced` | 12 | inheritance, polymorphism, `property`, dunder methods, ABCs |
| `async` | 10 | `async`/`await`, `asyncio.run`, `gather`, tasks |

**Total: 31 topics, ≈300 exercises.** Because topics are derived from directories, the curriculum is open-ended — a 32nd topic later is a content-only task, no code change.

### Exercise format

Unchanged from the hidden-checks design:

- `exercises/<topic>/<topic><N>.py` — the broken file the learner edits: a title comment, `# I AM NOT DONE`, a goal comment, and broken code.
- `checks/<topic>/<topic><N>.py` — the `assert` checks, hidden from the learner.

The existing `variables1`, `variables2`, and `functions1` stay and their topics expand around them.

### Difficulty rubric

Within each topic, exercises ramp:

- **1–3** — trivial intro: one concept, fill in a value or a single line.
- **4–7** — apply it: a small transformation or function.
- **8–10+** — combine concepts: a short challenge.

Each exercise covers **one clear concept**, is broken in an obvious way (a `???` placeholder, a missing line, a wrong value), and is solvable in a few lines. Because the checks are hidden, the **goal comment must fully state what is expected**.

**Example** — `exercises/loops/loops1.py`:

```python
# Exercise: Loops 1
# I AM NOT DONE
#
# Use a for-loop to add the numbers 1 through 5 into `total`.

total = 0
# write your loop here
```

`checks/loops/loops1.py`:

```python
assert total == 15, "total should be 1+2+3+4+5"
print("loops1 ✓")
```

### The `testing` topic

Testing exercises fit the same fix-the-broken-code loop, applied to writing tests. The learner writes code and its tests; the hidden check then runs and verifies them — e.g. given `add(a, b)`, complete a `test_add` that asserts the right things, and the check confirms `test_add` runs clean and actually exercises `add`. Exercises progress through `assert`, `pytest` test functions, `pytest.raises`, `parametrize`, and fixtures (conceptually).

---

## Testing

### Feature tests

- **Unit** — `State` v2 (flat `completed` set, `format_version` 2, graceful discard of a v1 file); `Manifest.topics()` and `exercises_in()` (grouping, first-appearance order).
- **TUI (Textual `Pilot`)** — the picker renders topics with `done/total`; selecting a topic enters its track; `F4` returns to the picker; finishing a topic's last exercise returns to the picker with the topic marked ✓.
- **CLI** — `list` (topics), `list <topic>`, `start <topic>`, `verify <topic>`, and unknown-topic errors.
- A small **multi-topic test fixture** is added — the current `tiny_curriculum` is single-topic, which cannot exercise the picker or topic grouping.

### Content QA

~300 exercises cannot each have a committed unit test. The QA contract: **every authored exercise must satisfy two properties — the broken form fails its check, and a known-correct solution passes it.** Each topic-authoring task verifies this for all of its exercises (apply a reference solution in a temp copy, run the runner, confirm pass; run the broken form, confirm fail).

`pylings verify` against the test fixtures remains the CI gate. The real 300-exercise curriculum is broken-by-design, so it is not a CI target; per-topic authoring verification is its QA.

---

## Implementation phasing

The plan is two phases.

### Phase 1 — the feature (~6 tasks)

1. `State` v2 — flat `completed` set, drop `current`, `format_version` 2.
2. `Manifest.topics()` / `exercises_in()` and topic-aware helpers.
3. CLI — `list` / `list <topic>` / `start <topic>` / `verify [<topic>]`; reset without the cursor rewind.
4. The multi-topic test fixture.
5. TUI — the topic-picker screen.
6. TUI — the track screen scoped to a topic, `F4` back-to-picker, topic-complete → picker.

After Phase 1, pylings is a working topic-navigation tool over the existing 3 exercises.

### Phase 2 — the content (31 tasks, one per topic)

Each task authors one topic: ~10 `exercises/<topic>/` files, ~10 `checks/<topic>/` files, the `info.toml` entries, verifies every exercise (broken fails / solved passes), and is independently shippable. Topics are authored in curriculum order. The `variables` and `functions` tasks expand the existing three exercises rather than starting empty.

≈ **37 tasks total.** Large, but every task is small and self-contained: Phase 1 ships the navigable tool; each Phase 2 task adds one complete topic.

---

## Success criteria

1. `pylings` opens a topic picker; selecting a topic enters its independent track.
2. A topic's progress (`done/total`) is tracked and shown independently of every other topic.
3. `pylings list`, `list <topic>`, `start <topic>`, `verify <topic>` all behave as specified; unknown topics error clearly.
4. `state.json` is `format_version` 2 with a flat `completed` set; an old v1 file is discarded gracefully.
5. The curriculum reaches 31 topics and ≈300 exercises; every exercise's broken form fails and a correct solution passes.
6. The full feature test suite (unit + TUI + CLI) is green; `pylings verify` passes against the fixtures; the cold-start guard still holds.
