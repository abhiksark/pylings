# Exercise: Dataclasses 7
# I AM NOT DONE
#
# A frozen dataclass is immutable: assigning to any field after
# construction raises a `FrozenInstanceError`.
#
# Fix `Config` by adding `frozen=True` to the `@dataclass` decorator.
# Fields: `host: str` and `port: int`.
#
# Hint: @dataclass(frozen=True)

from dataclasses import dataclass


@dataclass  # Bug: missing frozen=True
class Config:
    host: str
    port: int


cfg = Config("localhost", 8080)

try:
    cfg.port = 9090  # should raise because the dataclass is frozen
    mutation_raised = False
except Exception:
    mutation_raised = True
