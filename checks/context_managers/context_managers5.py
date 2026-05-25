assert result == {"dsn": "sqlite:///:memory:", "active": True}, (
    f"conn should be the connection dict, got {result!r}"
)
assert db.open is False, "__exit__ should set self.open to False"
print("context_managers5 ✓")
