# Exercise: Classes 12
# I AM NOT DONE
#
# Complete the BankAccount class so that all of the following work:
#
#   account = BankAccount("Alice", 100)
#   account.deposit(50)       -> balance becomes 150
#   account.withdraw(30)      -> balance becomes 120
#   account.withdraw(200)     -> raises ValueError ("insufficient funds")
#   str(account)              -> "BankAccount(Alice, balance=120)"
#
# Four things to fix:
#  1. `deposit` currently does nothing — make it add `amount` to balance.
#  2. `withdraw` currently does nothing — make it subtract `amount` from
#     balance, and raise ValueError("insufficient funds") if amount > balance.
#  3. `__str__` currently returns "" — return the correct string.
#  4. The class is missing `__init__` entirely — add it to store
#     `owner` and `balance` as instance attributes.

class BankAccount:
    def deposit(self, amount):
        pass

    def withdraw(self, amount):
        pass

    def __str__(self):
        return ""


account = BankAccount("Alice", 100)
account.deposit(50)
account.withdraw(30)
