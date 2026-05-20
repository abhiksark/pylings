# Exercise: Recursion 8
# ---------------------
# I AM NOT DONE
#
# A tree is represented as a dict with keys "value" (int) and
# "children" (list of trees, possibly empty).
#
# Complete two functions:
#
#   tree_depth(tree) — returns the depth of the tree.  A tree with no
#     children has depth 1.  Otherwise depth is 1 + max depth of children.
#
#   tree_search(tree, target) — returns True if `target` appears as a
#     "value" anywhere in the tree, False otherwise.
#
# Both must be recursive.

def tree_depth(tree):
    if not tree["children"]:
        return 1
    return ???


def tree_search(tree, target):
    if tree["value"] == target:
        return True
    return ???
