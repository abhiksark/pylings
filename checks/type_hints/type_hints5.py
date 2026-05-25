hints = bounding_box.__annotations__
assert hints.get("points") == list[tuple[float, float]], \
    "points should be annotated as list[tuple[float, float]]"
assert hints.get("return") == tuple[float, float, float, float], \
    "return type should be tuple[float, float, float, float]"
print("type_hints5 ✓")
