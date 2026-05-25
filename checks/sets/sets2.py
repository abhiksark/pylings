assert isinstance(colors, set), "colors should still be a set"
assert "purple" in colors, "'purple' was not added to colors"
assert "orange" not in colors, "'orange' was not removed from colors"
assert colors == {"red", "blue", "purple"}, f"colors should be {{'red', 'blue', 'purple'}}, got {colors!r}"
print("sets2 ✓")
