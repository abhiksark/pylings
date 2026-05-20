assert cfg.host == "localhost"
assert cfg.port == 8080
assert mutation_raised, (
    "assigning to a frozen dataclass field should raise FrozenInstanceError"
)
print("dataclasses7 ✓")
