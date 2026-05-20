test_user_greeting()

import inspect

def _code(fn):
    """Source of fn with comment lines removed — so guards can't be
    satisfied by words that only appear in the exercise's comments."""
    lines = inspect.getsource(fn).splitlines()
    return "\n".join(l for l in lines if not l.strip().startswith("#"))

src = _code(test_user_greeting)
assert "make_user" in src, "test_user_greeting should call make_user()"
assert "assert" in src, "test_user_greeting should contain assertions"
print("testing9 ✓")
