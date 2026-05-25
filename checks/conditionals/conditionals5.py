assert can_ride(130, True) == True, "tall + ticket => can ride"
assert can_ride(130, False) == False, "tall but no ticket => cannot ride"
assert can_ride(100, True) == False, "too short but has ticket => cannot ride"
assert can_ride(120, True) == True, "exactly 120 + ticket => can ride"
assert gets_discount(True, False) == True, "student => discount"
assert gets_discount(False, True) == True, "senior => discount"
assert gets_discount(True, True) == True, "student + senior => discount"
assert gets_discount(False, False) == False, "neither => no discount"
print("conditionals5 ✓")
