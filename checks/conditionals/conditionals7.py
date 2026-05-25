assert ticket_price(3, True) == 0, "under 5 is free"
assert ticket_price(0, False) == 0, "age 0 is free"
assert ticket_price(10, True) == 8, "adult member pays 8"
assert ticket_price(5, True) == 8, "exactly 5 + member pays 8"
assert ticket_price(10, False) == 12, "adult non-member pays 12"
assert ticket_price(5, False) == 12, "exactly 5 + non-member pays 12"
print("conditionals7 ✓")
