import dataclasses

assert v.x == 1.0 and v.y == 2.0 and v.z == 3.0
fields = {f.name for f in dataclasses.fields(Vector3)}
assert fields == {"x", "y", "z"}, f"expected fields x,y,z — got {fields}"
# The generated __init__ is created by @dataclass; verify it works for keyword args too.
v2 = Vector3(x=0.0, y=0.0, z=1.0)
assert v2.z == 1.0
print("dataclasses5 ✓")
