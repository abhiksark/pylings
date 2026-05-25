assert callable(square), "square should be a function"
assert square(4) == 16, f"Expected 16, got {square(4)}"
assert square(0) == 0
assert square(-3) == 9
assert square(2.5) == 6.25
print("functions4 ✓")
