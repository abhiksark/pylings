assert require_positive(5) == 5, f"expected 5, got {require_positive(5)!r}"
assert require_positive(1) == 1, f"expected 1, got {require_positive(1)!r}"

raised = False
try:
    require_positive(0)
except ValueError:
    raised = True
assert raised, "require_positive(0) should raise ValueError"

raised = False
try:
    require_positive(-3)
except ValueError:
    raised = True
assert raised, "require_positive(-3) should raise ValueError"
print("exceptions6 ✓")
