test_clamp()

import inspect
src = inspect.getsource(test_clamp)
assert src.count("assert") >= 5, "test_clamp should contain at least 5 assertions"
print("testing5 ✓")
