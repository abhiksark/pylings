assert deep_sum([]) == 0
assert deep_sum([1, 2, 3]) == 6
assert deep_sum([1, [2, 3]]) == 6
assert deep_sum([1, [2, 3], [4, [5]]]) == 15
assert deep_sum([[1, [2]], [3, [4, [5]]]]) == 15
assert deep_sum([10, [20, [30]]]) == 60
print("recursion7 ✓")
