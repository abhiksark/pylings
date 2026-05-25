# Exercise: Type Hints 8
# I AM NOT DONE
#
# Fully annotate the function `summarise`:
#   - parameter `records` should be annotated as `list[dict[str, int]]`
#   - parameter `key` should be annotated as `str`
#   - parameter `default` should be annotated as `int | None`
#   - the return type should be `dict[str, int | None]`
#
# The signature should read:
#   def summarise(
#       records: list[dict[str, int]],
#       key: str,
#       default: int | None,
#   ) -> dict[str, int | None]:

def summarise(records, key, default):
    return {
        "count": len(records),
        "total": sum(r.get(key, default or 0) for r in records),
        "missing": default,
    }
