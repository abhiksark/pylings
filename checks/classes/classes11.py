assert isinstance(t, Temperature), "from_string should return a Temperature instance"
assert t.degrees == 36.6, f"expected 36.6, got {t.degrees}"
assert boiling.degrees == 100.0
assert isinstance(Temperature.from_string("0C"), Temperature)
print("classes11 ✓")
