test_is_even()

import inspect
src = inspect.getsource(test_is_even)
assert src.count("assert") >= 4, "test_is_even should contain at least 4 assertions"
print("testing4 ✓")
