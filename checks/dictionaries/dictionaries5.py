assert isinstance(all_items, list), "all_items should be a list"
assert sorted(all_items) == ["eraser", "notebook", "pen"], f"all_items keys wrong: {all_items!r}"

assert isinstance(all_counts, list), "all_counts should be a list"
assert sorted(all_counts) == [5, 8, 10], f"all_counts values wrong: {all_counts!r}"

assert isinstance(all_pairs, list), "all_pairs should be a list"
assert sorted(all_pairs) == [("eraser", 8), ("notebook", 5), ("pen", 10)], (
    f"all_pairs tuples wrong: {all_pairs!r}"
)
print("dictionaries5 ✓")
