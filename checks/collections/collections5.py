assert p.x == 3, "p.x should be 3"
assert p.y == 4, "p.y should be 4"
assert p == (3, 4), "Point is still a tuple"
assert Point.__name__ == "Point", "type name should be Point"
print("collections5 ✓")
