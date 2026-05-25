assert is_terminal(TicketState.OPEN) is False
assert is_terminal(TicketState.CLOSED) is True
assert is_terminal(TicketState.CANCELLED) is True
print("enums5 ok")
