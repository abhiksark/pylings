assert "count" in __annotations__, "count should have a type annotation"
assert __annotations__["count"] is int, "count should be annotated as int"
print("type_hints1 ✓")
