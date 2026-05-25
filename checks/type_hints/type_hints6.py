assert "Vector" in dir() or "Vector" in globals(), "Vector type alias must be defined"
assert Vector == list[float], "Vector should equal list[float]"
hints = scale.__annotations__
assert hints.get("v") == list[float], "v should be annotated as Vector (list[float])"
assert hints.get("factor") is float, "factor should be annotated as float"
assert hints.get("return") == list[float], "return type should be Vector (list[float])"
print("type_hints6 ✓")
