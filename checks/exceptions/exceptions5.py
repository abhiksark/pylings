log.clear()
result = read_first([10, 20, 30])
assert result == 10, f"expected 10, got {result!r}"
assert log == ["done"], f"log should be ['done'] after a successful call, got {log!r}"

log.clear()
result = read_first([])
assert result is None, f"expected None, got {result!r}"
assert log == ["done"], f"log should be ['done'] even after an empty list, got {log!r}"
print("exceptions5 ✓")
