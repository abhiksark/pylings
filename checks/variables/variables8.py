assert kind is float, f"kind should be float (the type), got {kind}"
assert as_int == 3 and isinstance(as_int, int), f"as_int should be int 3, got {as_int!r}"
assert as_str == "42" and isinstance(as_str, str), f"as_str should be str '42', got {as_str!r}"
print("variables8 ✓")
