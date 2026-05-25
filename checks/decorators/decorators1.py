assert call_it(say_hello) == "hello", (
    f"call_it(say_hello) should return 'hello', got {call_it(say_hello)!r}"
)
assert call_it(give_seven) == 7, (
    f"call_it(give_seven) should return 7, got {call_it(give_seven)!r}"
)
assert call_it(lambda: 42) == 42
print("decorators1 ✓")
