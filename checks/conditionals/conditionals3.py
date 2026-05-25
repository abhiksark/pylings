assert grade(95) == "A", f"grade(95) should be 'A', got {grade(95)!r}"
assert grade(90) == "A", f"grade(90) should be 'A', got {grade(90)!r}"
assert grade(85) == "B", f"grade(85) should be 'B', got {grade(85)!r}"
assert grade(80) == "B", f"grade(80) should be 'B', got {grade(80)!r}"
assert grade(72) == "C", f"grade(72) should be 'C', got {grade(72)!r}"
assert grade(70) == "C", f"grade(70) should be 'C', got {grade(70)!r}"
assert grade(50) == "F", f"grade(50) should be 'F', got {grade(50)!r}"
assert grade(0) == "F", f"grade(0) should be 'F', got {grade(0)!r}"
print("conditionals3 ✓")
