assert sign(5) == "positive", f"sign(5) should be 'positive', got {sign(5)!r}"
assert sign(1) == "positive", f"sign(1) should be 'positive', got {sign(1)!r}"
assert sign(0) == "non-positive", f"sign(0) should be 'non-positive', got {sign(0)!r}"
assert sign(-3) == "non-positive", f"sign(-3) should be 'non-positive', got {sign(-3)!r}"
print("conditionals2 ✓")
