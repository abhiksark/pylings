assert right_val == 2, "pop() removes from the right — should be 2"
assert left_val == 0, "popleft() removes from the left — should be 0"
assert list(d) == [1], "one element remains in the deque"
print("collections7 ✓")
