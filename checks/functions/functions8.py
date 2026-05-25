assert callable(build_profile), "build_profile should be a function"
assert build_profile() == {}, f"build_profile() should return {{}}, got {build_profile()}"
assert build_profile(name="Alice", age=30) == {"name": "Alice", "age": 30}
assert build_profile(x=1) == {"x": 1}
assert build_profile(a=1, b=2, c=3) == {"a": 1, "b": 2, "c": 3}
print("functions8 ✓")
