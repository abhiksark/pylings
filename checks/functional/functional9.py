assert has_negative is True, f"has_negative should be True, got {has_negative}"
assert all_positive is True, f"all_positive should be True, got {all_positive}"

assert any(x < 0 for x in [1, 2, -3]) is True
assert any(x < 0 for x in [1, 2, 3]) is False
assert all(x > 0 for x in [1, 2, 3]) is True
assert all(x > 0 for x in [1, -2, 3]) is False
print("functional9 ✓")
