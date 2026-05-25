# Exercise: Type Hints 2
# I AM NOT DONE
#
# Annotate the function `greet` so that:
#   - parameter `name` is annotated as `str`
#   - parameter `times` is annotated as `int`
#   - the return type is annotated as `str`
#
# The signature should read:
#   def greet(name: str, times: int) -> str:

def greet(name, times):
    return (name + " ") * times
