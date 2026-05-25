# Exercise: Type Hints 4
# I AM NOT DONE
#
# Annotate the function `find_index` to express that a value might be absent:
#   - parameter `items` should be annotated as `list[str]`
#   - parameter `target` should be annotated as `str`
#   - the return type should be `int | None`  (the value or None when not found)
#
# The signature should read:
#   def find_index(items: list[str], target: str) -> int | None:

def find_index(items, target):
    try:
        return items.index(target)
    except ValueError:
        return None
