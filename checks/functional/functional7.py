triple = make_multiplier(3)
double = make_multiplier(2)

assert triple(4) == 12, f"triple(4) should be 12, got {triple(4)}"
assert double(7) == 14, f"double(7) should be 14, got {double(7)}"
assert make_multiplier(10)(5) == 50
assert callable(make_multiplier(1))
print("functional7 ✓")
