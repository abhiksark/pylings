import types

hints = summarise.__annotations__
assert hints.get("records") == list[dict[str, int]], \
    "records should be annotated as list[dict[str, int]]"
assert hints.get("key") is str, "key should be annotated as str"
default_hint = hints.get("default")
assert isinstance(default_hint, types.UnionType) and default_hint == (int | None), \
    "default should be annotated as int | None"
ret = hints.get("return")
assert ret == dict[str, int | None], \
    "return type should be dict[str, int | None]"
print("type_hints8 ✓")
