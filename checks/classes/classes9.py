assert repr(c) == "Color(r=255, g=128, b=0)", f"got {repr(c)!r}"
assert str(c) == "rgb(255, 128, 0)"
assert repr(Color(0, 0, 0)) == "Color(r=0, g=0, b=0)"
print("classes9 ✓")
