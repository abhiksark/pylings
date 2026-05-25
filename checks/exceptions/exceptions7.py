assert check_age(0) == 0, f"expected 0, got {check_age(0)!r}"
assert check_age(25) == 25, f"expected 25, got {check_age(25)!r}"
assert check_age(120) == 120, f"expected 120, got {check_age(120)!r}"

for bad in (-1, 121, 200):
    raised = False
    msg_ok = False
    try:
        check_age(bad)
    except ValueError as e:
        raised = True
        msg_ok = "age must be between 0 and 120" in str(e)
    assert raised, f"check_age({bad}) should raise ValueError"
    assert msg_ok, f"ValueError message should say 'age must be between 0 and 120'"
print("exceptions7 ✓")
