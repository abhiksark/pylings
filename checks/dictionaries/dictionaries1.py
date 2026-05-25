assert isinstance(ages, dict), "ages should be a dict"
assert ages == {"alice": 30, "bob": 25}, f"ages should map the two names to their ages, got {ages!r}"
print("dictionaries1 ✓")
