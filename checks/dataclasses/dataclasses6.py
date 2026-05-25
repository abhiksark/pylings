assert novel == copy, "two Books with the same fields should be equal"
assert novel != other, "Books with different fields should not be equal"
r = repr(novel)
assert "Dune" in r, f"repr should contain the title, got {r!r}"
assert "412" in r, f"repr should contain the page count, got {r!r}"
print("dataclasses6 ✓")
