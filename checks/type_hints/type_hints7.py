import typing

hints = apply_twice.__annotations__
expected_callable = typing.Callable[[int], int]
assert hints.get("func") == expected_callable, \
    f"func should be annotated as Callable[[int], int], got {hints.get('func')}"
assert hints.get("value") is int, "value should be annotated as int"
assert hints.get("return") is int, "return type should be int"
print("type_hints7 ✓")
