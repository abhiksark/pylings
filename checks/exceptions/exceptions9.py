assert issubclass(InsufficientFundsError, Exception), \
    "InsufficientFundsError must inherit from Exception"

assert withdraw(100, 30) == 70, f"expected 70, got {withdraw(100, 30)!r}"
assert withdraw(50, 50) == 0, f"expected 0, got {withdraw(50, 50)!r}"

raised = False
msg_ok = False
try:
    withdraw(20, 50)
except InsufficientFundsError as e:
    raised = True
    msg_ok = "50" in str(e) and "20" in str(e)
assert raised, "withdraw(20, 50) should raise InsufficientFundsError"
assert msg_ok, f"error message should mention both the amount (50) and balance (20)"
print("exceptions9 ✓")
