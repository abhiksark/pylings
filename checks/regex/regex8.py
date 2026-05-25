assert clean == "This email is full of *** and ***, total ***!", (
    f"clean should have spam and junk replaced, got: {clean!r}"
)
assert "spam" not in clean, "no 'spam' should remain"
assert "junk" not in clean, "no 'junk' should remain"
print("regex8 ✓")
