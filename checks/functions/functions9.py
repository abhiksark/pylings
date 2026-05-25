assert callable(min_max), "min_max should be a function"
assert min_max([3, 1, 4, 1, 5, 9]) == (1, 9)
assert min_max([7]) == (7, 7)
assert min_max([-5, 0, 5]) == (-5, 5)
assert lo == 1, f"lo should be 1 (the minimum), got {lo!r}. Did you unpack the tuple?"
assert hi == 9, f"hi should be 9 (the maximum), got {hi!r}. Did you unpack the tuple?"
print("functions9 ✓")
