assert loud_greet() == "HELLO", (
    f"loud_greet() should return 'HELLO', got {loud_greet()!r}"
)
assert shout(lambda: "world")() == "WORLD"
print("decorators2 ✓")
