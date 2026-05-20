test_parse_positive()

import inspect

def _code(fn):
    """Source of fn with comment lines removed — so guards can't be
    satisfied by words that only appear in the exercise's comments."""
    lines = inspect.getsource(fn).splitlines()
    return "\n".join(l for l in lines if not l.strip().startswith("#"))

src = _code(test_parse_positive)
assert "ValueError" in src, "test_parse_positive should reference ValueError"
assert "assert" in src, "test_parse_positive should contain assertions"
print("testing6 ✓")
