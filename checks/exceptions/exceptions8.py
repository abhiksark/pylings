assert classify_error(lambda: 1 + 1) == "ok", "no exception should return 'ok'"
assert classify_error(lambda: int("bad")) == "value error", "ValueError should return 'value error'"
assert classify_error(lambda: 1 + "x") == "type error", "TypeError should return 'type error'"
assert classify_error(lambda: (_ for _ in ()).throw(RuntimeError("boom"))) == "other error", \
    "other exceptions should return 'other error'"
print("exceptions8 ✓")
