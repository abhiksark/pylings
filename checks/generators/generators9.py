assert list(Counter(4)) == [0, 1, 2, 3]
assert list(Counter(1)) == [0]
assert list(Counter(0)) == []
# StopIteration must be raised at the right moment.
c = Counter(2)
assert next(c) == 0
assert next(c) == 1
try:
    next(c)
    raise AssertionError("expected StopIteration after stop elements")
except StopIteration:
    pass
print("generators9 ✓")
