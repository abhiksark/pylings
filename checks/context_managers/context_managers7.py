assert result == "not set", (
    f"ZeroDivisionError should have been suppressed; result={result!r}"
)

# A non-ZeroDivision error must still propagate.
import sys

_propagated = False
try:
    with SilentZeroDivision():
        raise ValueError("should propagate")
except ValueError:
    _propagated = True

assert _propagated, "ValueError should NOT be suppressed"
print("context_managers7 ✓")
