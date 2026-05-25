leaf = {"value": 7, "children": []}
single = {"value": 1, "children": []}
two_level = {"value": 1, "children": [{"value": 2, "children": []}, {"value": 3, "children": []}]}
deep = {"value": 1, "children": [{"value": 2, "children": [{"value": 3, "children": []}]}]}

assert tree_depth(single) == 1
assert tree_depth(two_level) == 2
assert tree_depth(deep) == 3

assert tree_search(leaf, 7) is True
assert tree_search(leaf, 99) is False
assert tree_search(two_level, 3) is True
assert tree_search(deep, 3) is True
assert tree_search(deep, 99) is False
print("recursion8 ✓")
