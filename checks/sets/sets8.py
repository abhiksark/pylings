assert isinstance(is_subset, bool), "is_subset should be a bool"
assert isinstance(is_superset, bool), "is_superset should be a bool"
assert is_subset is True, f"small IS a subset of big, is_subset should be True, got {is_subset!r}"
assert is_superset is True, f"big IS a superset of small, is_superset should be True, got {is_superset!r}"
print("sets8 ✓")
