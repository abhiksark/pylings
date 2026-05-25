assert has_apple is True, f"'apple' IS in fruits, has_apple should be True, got {has_apple!r}"
assert has_grape is False, f"'grape' is NOT in fruits, has_grape should be False, got {has_grape!r}"
assert isinstance(has_apple, bool), "has_apple should be a bool"
assert isinstance(has_grape, bool), "has_grape should be a bool"
print("sets3 ✓")
