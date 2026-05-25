expected = [32.0, 212.0, -40.0, 98.6, 413.6, -459.4]
assert len(fahrenheit) == len(expected), (
    f"fahrenheit should have {len(expected)} elements, got {len(fahrenheit)}"
)
for i, (got, want) in enumerate(zip(fahrenheit, expected)):
    assert abs(got - want) < 1e-9, f"fahrenheit[{i}]: expected {want}, got {got}"
print("lists8 ✓")
