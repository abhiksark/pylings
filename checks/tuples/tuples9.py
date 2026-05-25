assert grid[(0, 0)] == "origin", f"grid[(0,0)] should be 'origin', got {grid.get((0,0))!r}"
assert grid[(1, 0)] == "right", f"grid[(1,0)] should be 'right', got {grid.get((1,0))!r}"
assert grid[(0, 1)] == "up", f"grid[(0,1)] should be 'up', got {grid.get((0,1))!r}"
assert label == "right", f"label should be 'right', got {label!r}"
print("tuples9 ✓")
