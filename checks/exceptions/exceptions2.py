assert parse_number("42") == 42, f"expected 42, got {parse_number('42')!r}"
assert parse_number("0") == 0, f"expected 0, got {parse_number('0')!r}"
assert parse_number("abc") == -1, f"expected -1, got {parse_number('abc')!r}"
assert parse_number("3.14") == -1, f"expected -1, got {parse_number('3.14')!r}"
print("exceptions2 ✓")
