hints = find_index.__annotations__
assert hints.get("items") == "list[str]", "items should be annotated as list[str]"
assert hints.get("target") == "str", "target should be annotated as str"
assert hints.get("return") == "int | None", "return type should be int | None"
print("type_hints4 ✓")
