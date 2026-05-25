assert "banana" not in basket, "'banana' should have been removed from basket"
assert "cherry" not in basket, "'cherry' should have been removed from basket"
assert cherry_count == 12, f"cherry_count should be 12, got {cherry_count!r}"
assert basket == {"apple": 5, "date": 7}, f"basket should only have apple and date left, got {basket!r}"
print("dictionaries4 ✓")
