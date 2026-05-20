test_parse_positive()

import inspect
src = inspect.getsource(test_parse_positive)
assert "ValueError" in src, "test_parse_positive should reference ValueError"
assert "assert" in src, "test_parse_positive should contain assertions"
print("testing6 ✓")
