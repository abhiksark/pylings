test_divide_message()

import inspect

def _code(fn):
    """Source of fn with comment lines removed — so guards can't be
    satisfied by words that only appear in the exercise's comments."""
    lines = inspect.getsource(fn).splitlines()
    return "\n".join(l for l in lines if not l.strip().startswith("#"))

src = _code(test_divide_message)
assert "ValueError" in src, "test_divide_message should reference ValueError"
assert '"zero"' in src or "'zero'" in src, "test_divide_message should check the message contains 'zero'"
print("testing7 ✓")
