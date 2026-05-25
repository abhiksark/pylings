assert isinstance(pairs, list), "pairs should be a list"
assert pairs == [
    (0, 0), (0, 1), (0, 2),
    (1, 0), (1, 1), (1, 2),
], f"unexpected pairs: {pairs!r}"
print("comprehensions4 ✓")
