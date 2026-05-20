test_divide_message()

import inspect
src = inspect.getsource(test_divide_message)
assert "ValueError" in src, "test_divide_message should reference ValueError"
assert '"zero"' in src or "'zero'" in src, "test_divide_message should check the message contains 'zero'"
print("testing7 ✓")
