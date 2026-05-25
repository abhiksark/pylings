assert isinstance(labels, list), "labels should be a list"
assert labels == ["odd", "even", "odd", "even", "odd", "even"], (
    f"expected ['odd', 'even', 'odd', 'even', 'odd', 'even'], got {labels!r}"
)
print("comprehensions8 ✓")
