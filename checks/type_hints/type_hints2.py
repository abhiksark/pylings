hints = greet.__annotations__
assert hints.get("name") is str, "name should be annotated as str"
assert hints.get("times") is int, "times should be annotated as int"
assert hints.get("return") is str, "the return type should be str"
print("type_hints2 ✓")
