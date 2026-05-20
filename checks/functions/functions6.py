assert callable(describe_pet), "describe_pet should be a function"
assert describe_pet("Buddy", "dog") == "My dog is named Buddy."
assert describe_pet(animal_type="cat", name="Whiskers") == "My cat is named Whiskers."
assert description == "My dog is named Buddy.", (
    f"Expected 'My dog is named Buddy.' but got {description!r}. "
    "Use keyword arguments to fix the call."
)
print("functions6 ✓")
