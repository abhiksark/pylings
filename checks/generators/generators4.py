import types

assert isinstance(cube_gen, types.GeneratorType), (
    f"cube_gen must be a generator, got {type(cube_gen)}"
)
assert list(cube_gen) == [1, 8, 27, 64, 125], (
    "cube_gen should yield 1, 8, 27, 64, 125"
)
print("generators4 ✓")
