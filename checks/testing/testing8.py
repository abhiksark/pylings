test_fahrenheit_to_celsius()

import inspect
src = inspect.getsource(test_fahrenheit_to_celsius)
# ensure cases list is not empty by checking at least 4 tuples are present
assert src.count("(") >= 5, "cases list should contain at least 4 tuples"
assert "for" in src, "test should loop over cases"
# run a direct spot check
assert abs(fahrenheit_to_celsius(32) - 0.0) < 1e-6
assert abs(fahrenheit_to_celsius(212) - 100.0) < 1e-6
assert abs(fahrenheit_to_celsius(-40) - (-40.0)) < 1e-6
print("testing8 ✓")
