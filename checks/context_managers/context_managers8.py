assert in_block_acquired is True, "resource should be acquired inside the with-block"
assert r.acquired is False, "resource should be released after the with-block"
assert r.release_log == ["released"], (
    f"release_log should be ['released'], got {r.release_log!r}"
)

# Re-entrant: acquire and release again.
with ManagedPool(r) as res2:
    pass

assert r.acquired is False
assert r.release_log == ["released", "released"], (
    f"release_log should have two entries after two uses, got {r.release_log!r}"
)
print("context_managers8 ✓")
