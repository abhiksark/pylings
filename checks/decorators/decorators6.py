assert compute(2, 3) == 5
assert compute.__name__ == "compute", (
    f"__name__ should be 'compute', got {compute.__name__!r}"
)
assert compute.__doc__ == "Return the sum of x and y.", (
    f"__doc__ should be preserved, got {compute.__doc__!r}"
)
print("decorators6 ✓")
