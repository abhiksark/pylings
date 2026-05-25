import types

hints = find_index.__annotations__
assert hints.get("items") == list[str], "items should be annotated as list[str]"
assert hints.get("target") is str, "target should be annotated as str"
ret = hints.get("return")
assert isinstance(ret, types.UnionType) and ret == (int | None), \
    "return type should be int | None"
print("type_hints4 ✓")
