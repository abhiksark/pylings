assert safe_divide(10, 2) == 5.0, f"expected 5.0, got {safe_divide(10, 2)!r}"
assert safe_divide(7, 0) == "error", f"expected 'error', got {safe_divide(7, 0)!r}"
assert safe_divide(9, 3) == 3.0, f"expected 3.0, got {safe_divide(9, 3)!r}"
print("exceptions1 ✓")
