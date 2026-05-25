assert account.owner == "Alice", f"owner should be 'Alice', got {account.owner!r}"
assert account.balance == 120, f"balance should be 120 after deposit 50 and withdraw 30, got {account.balance}"
assert str(account) == "BankAccount(Alice, balance=120)", f"got {str(account)!r}"

fresh = BankAccount("Bob", 50)
fresh.deposit(25)
assert fresh.balance == 75

import sys
try:
    fresh.withdraw(1000)
    assert False, "should have raised ValueError"
except ValueError as e:
    assert "insufficient" in str(e).lower(), f"ValueError message should mention 'insufficient', got {e!r}"

print("classes12 ✓")
