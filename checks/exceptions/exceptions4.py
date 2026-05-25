assert load_value({"x": 5}, "x") == 10, f"expected 10, got {load_value({'x': 5}, 'x')!r}"
assert load_value({"x": 5}, "y") == "missing", f"expected 'missing', got {load_value({'x': 5}, 'y')!r}"
assert load_value({"a": 3, "b": 7}, "b") == 14, f"expected 14, got {load_value({'a': 3, 'b': 7}, 'b')!r}"
assert load_value({}, "z") == "missing", f"expected 'missing', got {load_value({}, 'z')!r}"
print("exceptions4 ✓")
