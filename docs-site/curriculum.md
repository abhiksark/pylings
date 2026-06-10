# Curriculum

Pythonlings ships 292 exercises across 31 topics. Each exercise has a learner file,
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
original snapshot created during `pythonlings init`.
