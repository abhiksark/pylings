assert compare(1, 2) == "less", f"compare(1, 2) should be 'less', got {compare(1, 2)!r}"
assert compare(5, 5) == "equal", f"compare(5, 5) should be 'equal', got {compare(5, 5)!r}"
assert compare(9, 3) == "greater", f"compare(9, 3) should be 'greater', got {compare(9, 3)!r}"
assert compare(0, 0) == "equal", f"compare(0, 0) should be 'equal', got {compare(0, 0)!r}"
assert compare(-1, 0) == "less", f"compare(-1, 0) should be 'less', got {compare(-1, 0)!r}"
assert compare(100, 99) == "greater", f"compare(100, 99) should be 'greater', got {compare(100, 99)!r}"
print("conditionals4 ✓")
