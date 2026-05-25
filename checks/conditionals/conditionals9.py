assert absolute(5) == 5, f"absolute(5) should be 5, got {absolute(5)!r}"
assert absolute(-5) == 5, f"absolute(-5) should be 5, got {absolute(-5)!r}"
assert absolute(0) == 0, f"absolute(0) should be 0, got {absolute(0)!r}"
assert absolute(-100) == 100, f"absolute(-100) should be 100, got {absolute(-100)!r}"
assert absolute(3.5) == 3.5, f"absolute(3.5) should be 3.5, got {absolute(3.5)!r}"
assert absolute(-3.5) == 3.5, f"absolute(-3.5) should be 3.5, got {absolute(-3.5)!r}"
print("conditionals9 ✓")
