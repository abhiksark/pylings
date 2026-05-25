assert top_student == "Diana", f"top_student should be 'Diana', got {top_student!r}"
assert average == 71.0, f"average should be 71.0, got {average!r}"
assert passed == ["Alice", "Diana", "Eve"], (
    f"passed should be ['Alice', 'Diana', 'Eve'], got {passed!r}"
)
print("tuples10 ✓")
