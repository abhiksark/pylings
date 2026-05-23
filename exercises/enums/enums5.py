# Exercise: Enums 5
# I AM NOT DONE
#
# Goal: Return True only for terminal ticket states.

from enum import Enum, auto

class TicketState(Enum):
    OPEN = auto()
    CLOSED = auto()
    CANCELLED = auto()

def is_terminal(state):
    return ???
