# Exercise: Context Managers 5
# I AM NOT DONE
#
# `__enter__` can return any value; that value becomes the target of the
# `as` clause.  Fix `DatabaseConnection` so that `with db as conn:` gives
# the caller a dict that they can use like a connection.
#
# `__enter__` should return `self.connection` (the dict already set up in
# `__init__`).  `__exit__` should set `self.open` to False.
#
# Hint: `def __enter__(self): return self.connection`


class DatabaseConnection:
    def __init__(self, dsn):
        self.dsn = dsn
        self.open = True
        self.connection = {"dsn": dsn, "active": True}

    def __enter__(self):
        # Bug: returns None instead of self.connection.
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.open = False


db = DatabaseConnection("sqlite:///:memory:")
with db as conn:
    result = conn
