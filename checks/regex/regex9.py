assert match is not None, "pattern should match '2024-07-15'"
assert year == "2024", f"year should be '2024', got {year!r}"
assert month == "07", f"month should be '07', got {month!r}"
assert day == "15", f"day should be '15', got {day!r}"
m2 = re.search(pattern, "1999-12-31")
assert m2 is not None
assert m2.group("year") == "1999" and m2.group("month") == "12" and m2.group("day") == "31"
print("regex9 ✓")
