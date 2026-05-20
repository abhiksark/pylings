assert isinstance(unique_lengths, set), "unique_lengths should be a set"
assert unique_lengths == {3, 5, 8}, f"expected {{3, 5, 8}}, got {unique_lengths!r}"
print("comprehensions6 ✓")
