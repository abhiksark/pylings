assert isinstance(unique, set), "unique should be a set"
assert unique == {1, 2, 3, 4, 5}, f"unique should be {{1, 2, 3, 4, 5}}, got {unique!r}"
assert isinstance(unique_count, int), "unique_count should be an int"
assert unique_count == 5, f"unique_count should be 5, got {unique_count!r}"
print("sets7 ✓")
