test_fahrenheit_to_celsius()

import inspect, textwrap

def _code(fn):
    """Source of fn with comment lines removed — so guards can't be
    satisfied by words that only appear in the exercise's comments."""
    lines = inspect.getsource(fn).splitlines()
    return "\n".join(l for l in lines if not l.strip().startswith("#"))

src = _code(test_fahrenheit_to_celsius)
assert "for" in src, "test should loop over cases"

# Extract the cases list by running the function body in isolation
_body = textwrap.dedent(
    "\n".join(src.splitlines()[1:])  # skip the def line
)
_ns = {"fahrenheit_to_celsius": fahrenheit_to_celsius}
exec(_body, _ns)
cases = _ns.get("cases", [])
assert len(cases) >= 3, "cases should hold at least 3 (input, expected) pairs"

# run a direct spot check
assert abs(fahrenheit_to_celsius(32) - 0.0) < 1e-6
assert abs(fahrenheit_to_celsius(212) - 100.0) < 1e-6
assert abs(fahrenheit_to_celsius(-40) - (-40.0)) < 1e-6
print("testing8 ✓")
