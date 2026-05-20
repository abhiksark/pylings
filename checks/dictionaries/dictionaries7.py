assert isinstance(discounted, dict), "discounted should be a dict"
assert discounted == {"apple": 0.9, "milk": 1.35, "bread": 2.25}, (
    f"discounted wrong: {discounted!r}"
)
print("dictionaries7 ✓")
