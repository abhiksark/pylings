assert count_items([]) == 0
assert count_items([42]) == 1
assert count_items([1, 2, 3]) == 3
assert count_items(["a", "b", "c", "d"]) == 4
assert count_items(list(range(10))) == 10
print("recursion4 ✓")
