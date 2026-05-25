test_counter()

import inspect
src = inspect.getsource(test_counter)
assert "Counter" in src, "test_counter should instantiate Counter"
assert src.count("assert") >= 4, "test_counter should contain at least 4 assertions"
print("testing11 ✓")
