assert isinstance(result, list), f"result should be a list, got {type(result)}"
assert result == [1, 4, 9, 16, 25], f"expected [1, 4, 9, 16, 25], got {result}"
print("generators2 ✓")
