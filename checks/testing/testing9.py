test_user_greeting()

import inspect
src = inspect.getsource(test_user_greeting)
assert "make_user" in src, "test_user_greeting should call make_user()"
assert "assert" in src, "test_user_greeting should contain assertions"
print("testing9 ✓")
