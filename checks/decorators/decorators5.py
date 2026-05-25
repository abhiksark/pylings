assert add(3, 4) == 7, f"add(3, 4) should return 7, got {add(3, 4)!r}"
assert add(10, -2) == 8
assert greet("Alice") == "Hello, Alice!"
assert greet("Bob", greeting="Hi") == "Hi, Bob!"
print("decorators5 ✓")
