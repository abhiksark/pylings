assert callable(make_greeting), "make_greeting should be a function"
assert make_greeting("Alice") == "Hello, Alice!"
assert make_greeting("Bob", "Hi") == "Hi, Bob!"
assert make_greeting("World") == "Hello, World!"
assert make_greeting("Eve", "Hey") == "Hey, Eve!"
print("functions5 ✓")
