assert first == "a", f"first should be 'a', got {first!r}"
assert second == "b", f"second should be 'b', got {second!r}"
assert third == "c", f"third should be 'c', got {third!r}"
# The generator should now be exhausted.
try:
    next(gen)
    raise AssertionError("generator should be exhausted after three next() calls")
except StopIteration:
    pass
print("generators5 ✓")
