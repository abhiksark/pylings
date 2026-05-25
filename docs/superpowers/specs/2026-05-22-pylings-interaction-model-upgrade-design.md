# Pylings — Interaction Model Upgrade Design

**Date:** 2026-05-22
**Status:** Approved for implementation
**Owner:** abhiksark@gmail.com
**Builds on:** `2026-05-19-pylings-rustlings-ux-design.md`, `2026-05-20-pylings-builtin-editor-design.md`, `2026-05-20-pylings-topics-and-curriculum-design.md`

## Goal

Make pylings feel intuitive for beginners from first launch through repeated practice. The upgraded interaction model should orient new learners, resume returning learners directly into useful work, make the editor/check loop self-explanatory, and keep success fast.

## Non-goals

- A full tutorial framework.
- Rich IDE features such as completion, linting, or multi-file editing.
- Changing exercise/check execution semantics.
- Reworking curriculum content beyond reading existing goal comments where available.
- Replacing the existing Textual architecture.

## Decisions

| Area | Decision |
|---|---|
| Implementation scope | Interaction model upgrade |
| First launch | Smart Picker with compact onboarding and a highlighted "Start here" topic |
| Returning launch | Resume directly into the last active exercise when possible |
| Topic access | `F4` always returns to topics; add `pylings topics` as explicit picker command |
| Topic picker | Smart Picker with state-aware banner, row status labels, and useful initial selection |
| Solve loop | Guided Panel replaces raw-output-first panel |
| Hints | Progressive hints: hint availability first, short nudge after failure, full hint on `F1` |
| Success | Instant advance to the next exercise |
| Testing | Cover state, CLI, picker, track, panel states, hints, and full suite |

## UX State

Keep the existing `format_version = 2` state file and extend it with optional fields so existing local progress continues to load.

```json
{
  "format_version": 2,
  "completed": ["variables1"],
  "seen_intro": true,
  "last_topic": "variables",
  "last_exercise": "variables2"
}
```

Rules:

- Missing `seen_intro` defaults to `false`.
- Missing `last_topic` and `last_exercise` default to `null`.
- `completed` remains the source of truth for progress.
- Invalid resume pointers are ignored at launch time rather than corrupting progress.
- State writes remain atomic.

## Launch Flow

`pylings` decides between orientation and direct work:

1. If `seen_intro` is false, open the Smart Picker.
2. In the picker, show first-run orientation and highlight the first incomplete topic as "Start here."
3. When a topic is opened, set `seen_intro = true`, `last_topic`, and the current `last_exercise`.
4. On later launches, try to resume directly into `last_exercise` if it exists and is incomplete.
5. If `last_exercise` is complete or missing, resume to the next pending exercise in `last_topic`.
6. If `last_topic` is complete or invalid, open the Smart Picker with a "Choose what to practice next" banner.
7. `pylings topics` always opens the Smart Picker, regardless of resume state.

The existing `pylings start <topic>` command remains a direct jump to a topic track and also updates resume state.

## Smart Picker

The topic picker becomes an orientation and navigation surface.

Banner states:

- First run: `Start here: <topic>`
- No progress but intro already seen: `Choose a topic to practice.`
- Returning via `F4`: `Topics`
- Topic just completed: `Nice. Pick another topic.`
- All topics complete: use the manifest final message when available.

Rows show:

- Status marker: complete, started/current, or untouched.
- Topic name.
- `done/total`.
- Status label: `Start`, `Continue`, or `Done`.

Initial selection:

- `last_topic` when present and incomplete.
- First incomplete topic otherwise.
- First topic when no progress exists.

`Enter` opens the selected topic and records `last_topic`.

## Track Screen

The track screen keeps the current editor/output layout and linear per-topic progression.

Changes:

- On mount, choose the current exercise from resume state when valid, otherwise first pending in the topic.
- Persist `last_topic` and `last_exercise` whenever an exercise is loaded.
- `F4` flushes pending edits, updates resume state, and returns to the picker.
- `Ctrl+Q` flushes pending edits and keeps resume state pointing at the current exercise.
- Completing an exercise marks it done, immediately loads the next exercise, updates progress, and persists the new resume target.
- Completing the last exercise in a topic clears `last_exercise` and returns to the picker or shows a topic-complete state that immediately points the learner back to topics.

## Guided Panel

The output panel should stop presenting raw tracebacks as the primary UI. It becomes a Guided Panel with predictable sections.

Header:

- Exercise name.
- Topic progress.
- Short file path.

Sections:

- **Goal:** extracted from leading exercise comments when available. If no goal comment is found, use the exercise name.
- **Status:** one of `Editing`, `Running checks...`, `Not passing yet`, `Checks pass, remove marker`, or `Complete`.
- **Next step:** a concrete learner-facing action.
- **Details:** raw stdout/stderr for learners who need the real Python output.
- **Hint:** hidden full hint toggled by `F1`.

Failure handling:

- Timeout: next step explains likely infinite loop.
- Non-zero exit: next step points to the details section.
- Passing checks with marker still present: next step tells the learner to remove `# I AM NOT DONE`.
- Passing without marker: show complete state very briefly only as part of the instant load path, then load the next exercise.

Running state:

- When a debounced save starts a run, show `Running checks...` so delayed runs do not feel broken.

## Progressive Hints

Hints stay useful without becoming the default solution path.

- Before any failure, the panel says a hint is available via `F1`.
- After the first failed run for an exercise, show a short nudge.
- The short nudge uses the first sentence of the manifest hint when available.
- `F1` toggles the full manifest hint.
- Full hint never appears by default.
- Loading a new exercise resets the failure count and hint visibility.

## CLI

Add:

| Command | Behavior |
|---|---|
| `pylings topics` | Launch the TUI on the Smart Picker |

Existing commands keep their current behavior. `pylings` uses resume logic, `pylings watch` is an alias for default launch behavior, and `pylings start <topic>` jumps directly to a topic track.

## Error Handling

- Invalid `last_topic` or `last_exercise` values are ignored.
- Missing goal comments fall back to exercise name.
- State corruption keeps the existing backup-and-reset behavior.
- Runtime failures still come from the runner as `RunResult`.
- State write failures should surface; progress must not be silently discarded.

## Testing

Tests should cover:

- State load/save with optional UX fields.
- Backward-compatible load from existing v2 state without UX fields.
- First-run `pylings` opens the Smart Picker and marks intro seen when a topic is opened.
- Returning `pylings` resumes directly into the last active incomplete exercise.
- Invalid resume state falls back to the picker.
- `pylings topics` opens the Smart Picker.
- `F4` returns from track to picker.
- Picker row labels and initial selection.
- Guided Panel states for running, failure, marker-present pass, and complete.
- Progressive hints before failure, after failure, and after `F1`.
- Instant advance after solving an exercise.
- Full suite passes with `pytest`.
