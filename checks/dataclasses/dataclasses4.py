assert b1.items == ["apple"], f"b1.items = {b1.items!r}"
assert b2.items == [], f"b2.items should still be empty, got {b2.items!r}"
print("dataclasses4 ✓")
