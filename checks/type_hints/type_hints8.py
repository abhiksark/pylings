hints = summarise.__annotations__
assert hints.get("records") == "list[dict[str, int]]", \
    "records should be annotated as list[dict[str, int]]"
assert hints.get("key") == "str", "key should be annotated as str"
assert hints.get("default") == "int | None", \
    "default should be annotated as int | None"
assert hints.get("return") == "dict[str, int | None]", \
    "return type should be dict[str, int | None]"
print("type_hints8 ✓")
