# Pylings Roadmap Curriculum Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the seven missing specialized roadmap topics so pylings reaches 31 topics and 292 exercises.

**Architecture:** This is a content-only curriculum expansion plus manifest coverage tests. The existing manifest, runner, TUI, state, and hidden-check architecture remain unchanged.

**Tech Stack:** Python 3.11+, TOML manifest (`info.toml`), pytest.

---

## File Structure

- Modify `info.toml`: append 58 `[[exercises]]` entries after `collections10`.
- Create `exercises/itertools/itertools1.py` through `itertools8.py`.
- Create `checks/itertools/itertools1.py` through `itertools8.py`.
- Create `exercises/json/json1.py` through `json8.py`.
- Create `checks/json/json1.py` through `json8.py`.
- Create `exercises/datetime/datetime1.py` through `datetime8.py`.
- Create `checks/datetime/datetime1.py` through `datetime8.py`.
- Create `exercises/enums/enums1.py` through `enums6.py`.
- Create `checks/enums/enums1.py` through `enums6.py`.
- Create `exercises/pathlib/pathlib1.py` through `pathlib6.py`.
- Create `checks/pathlib/pathlib1.py` through `pathlib6.py`.
- Create `exercises/oop_advanced/oop_advanced1.py` through `oop_advanced12.py`.
- Create `checks/oop_advanced/oop_advanced1.py` through `oop_advanced12.py`.
- Create `exercises/async/async1.py` through `async10.py`.
- Create `checks/async/async1.py` through `async10.py`.
- Modify `tests/unit/test_manifest.py`: add real curriculum coverage tests.

---

### Task 1: Real Curriculum Coverage Test

**Files:**
- Modify: `tests/unit/test_manifest.py`

- [ ] **Step 1: Add failing tests**

Add tests that load the repository root curriculum and assert the target topic/exercise counts:

```python
def test_real_curriculum_has_roadmap_topic_counts() -> None:
    repo = Path(__file__).parents[2]
    manifest = load(repo)
    expected = {
        "itertools": 8,
        "json": 8,
        "datetime": 8,
        "enums": 6,
        "pathlib": 6,
        "oop_advanced": 12,
        "async": 10,
    }
    assert len(manifest.exercises) == 292
    assert len(manifest.topics()) == 31
    for topic, count in expected.items():
        assert len(manifest.exercises_in(topic)) == count


def test_real_curriculum_check_files_parse() -> None:
    import ast

    repo = Path(__file__).parents[2]
    manifest = load(repo)
    for exercise in manifest.exercises:
        ast.parse(
            exercise.check_path.read_text(encoding="utf-8"),
            filename=str(exercise.check_path),
        )
```

- [ ] **Step 2: Verify red**

Run: `.venv/bin/python -m pytest tests/unit/test_manifest.py::test_real_curriculum_has_roadmap_topic_counts -q`

Expected: FAIL because the repository currently has 234 exercises and 24 topics.

---

### Task 2: Add Specialized Topics

**Files:**
- Modify: `info.toml`
- Create all exercise/check files listed in File Structure.

- [ ] **Step 1: Author topic content**

Add the seven topics in this order with the exact counts from the spec:

1. `itertools` - 8 exercises
2. `json` - 8 exercises
3. `datetime` - 8 exercises
4. `enums` - 6 exercises
5. `pathlib` - 6 exercises
6. `oop_advanced` - 12 exercises
7. `async` - 10 exercises

Each exercise must include a clear goal comment and `# I AM NOT DONE`. Each check must contain assertions and a short success print.

- [ ] **Step 2: Keep manifest naming consistent**

For every exercise `topicN`, append:

```toml
[[exercises]]
name = "topicN"
path = "exercises/topic/topicN.py"
hint = "Use the topic concept named in the goal comment to produce the checked value."
```

Use real topic names and real hints for every entry.

---

### Task 3: Verify And Commit

**Files:**
- All files from Tasks 1-2.

- [ ] **Step 1: Run targeted manifest coverage**

Run: `.venv/bin/python -m pytest tests/unit/test_manifest.py::test_real_curriculum_has_roadmap_topic_counts tests/unit/test_manifest.py::test_real_curriculum_check_files_parse -q`

Expected: PASS.

- [ ] **Step 2: Run full test suite**

Run: `.venv/bin/python -m pytest -q`

Expected: PASS.

- [ ] **Step 3: Commit**

Run:

```bash
git add info.toml exercises checks tests/unit/test_manifest.py
git commit -m "feat: complete roadmap curriculum topics"
```
