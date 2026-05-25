result = say("hi")
assert result == "hi", f"say('hi') should return 'hi', got {result!r}"

# The function should have been called 3 times (side-effect: last result returned)
assert identity(99) == 99
assert identity("abc") == "abc"

# Verify repeat with a counter to confirm n calls happen
call_log = []

@repeat(4)
def tracked(x):
    call_log.append(x)
    return x

tracked(1)
assert len(call_log) == 4, (
    f"repeat(4) should call the function 4 times, got {len(call_log)}"
)
print("decorators8 ✓")
