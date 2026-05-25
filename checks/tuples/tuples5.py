assert original == (10, 20, 30), "original must not be changed"
assert isinstance(updated, tuple), "updated should be a tuple"
assert updated == (10, 99, 30), f"updated should be (10, 99, 30), got {updated!r}"
print("tuples5 ✓")
