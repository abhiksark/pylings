assert c.count == 3, f"count should be 3 after three increments, got {c.count}"
d = Counter()
d.increment()
assert d.count == 1
print("classes5 ✓")
