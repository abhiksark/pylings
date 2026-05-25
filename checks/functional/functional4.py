assert evens == [2, 4, 6, 8, 10], f"evens should be [2, 4, 6, 8, 10], got {evens}"
assert isinstance(evens, list)
assert all(x % 2 == 0 for x in evens)
print("functional4 ✓")
