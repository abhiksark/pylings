hints = total.__annotations__
assert hints.get("scores") == list[int], "scores should be annotated as list[int]"
assert hints.get("labels") == dict[str, int], "labels should be annotated as dict[str, int]"
assert hints.get("return") is int, "the return type should be int"
print("type_hints3 ✓")
