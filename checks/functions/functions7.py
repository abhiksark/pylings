assert callable(total), "total should be a function"
assert total() == 0, f"total() should be 0, got {total()}"
assert total(5) == 5, f"total(5) should be 5, got {total(5)}"
assert total(1, 2, 3) == 6, f"total(1,2,3) should be 6, got {total(1,2,3)}"
assert total(10, 20, 30, 40) == 100
assert total(-1, 1) == 0
print("functions7 ✓")
