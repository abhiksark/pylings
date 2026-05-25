assert isinstance(vowels, list), "vowels should be a list"
expected = [c for c in "list comprehensions are quite powerful" if c in "aeiou"]
assert vowels == expected, f"expected {expected!r}, got {vowels!r}"
print("comprehensions7 ✓")
