assert isinstance(result, tuple), "min_max should return a tuple"
assert result == (1, 9), f"min_max([4,1,7,2,9,3]) should return (1, 9), got {result!r}"
lo, hi = min_max([3, 3, 3])
assert lo == 3 and hi == 3, "min_max should work when all values are equal"
print("tuples6 ✓")
