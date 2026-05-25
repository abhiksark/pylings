assert add.call_count == 0
add(1, 2)
assert add.call_count == 1, (
    f"call_count should be 1 after one call, got {add.call_count}"
)
add(3, 4)
add(5, 6)
assert add.call_count == 3, (
    f"call_count should be 3 after three calls, got {add.call_count}"
)
assert add(10, 20) == 30
print("decorators7 ✓")
