test_add()

import inspect

def _code(fn):
    """Source of fn with comment lines removed — so guards can't be
    satisfied by words that only appear in the exercise's comments."""
    lines = inspect.getsource(fn).splitlines()
    return "\n".join(l for l in lines if not l.strip().startswith("#"))

assert "assert" in _code(test_add), "test_add should contain assertions"
print("testing3 ✓")
