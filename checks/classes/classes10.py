assert Circle.pi == 3.14159, "pi should be a class attribute on Circle"
assert abs(c1.area() - 3.14159) < 1e-6, f"area of circle r=1 should be ~3.14159, got {c1.area()}"
assert abs(c2.area() - 3.14159 * 25) < 1e-4
assert c1.pi is c2.pi, "pi should be the same class-level object for all instances"
print("classes10 ✓")
