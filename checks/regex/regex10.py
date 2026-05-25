assert match is not None, "pattern should match the log line"
assert level == "ERROR", f"level should be 'ERROR', got {level!r}"
assert logger == "db.engine", f"logger should be 'db.engine', got {logger!r}"
assert message == "connection refused", f"message should be 'connection refused', got {message!r}"

m2 = re.search(pattern, "[WARNING] app.server: disk usage at 90%")
assert m2 is not None, "pattern should match a WARNING line"
assert m2.group("level") == "WARNING"
assert m2.group("logger") == "app.server"
assert m2.group("message") == "disk usage at 90%"

m3 = re.search(pattern, "[INFO] scheduler: job completed in 0.5s")
assert m3 is not None, "pattern should match an INFO line"
assert m3.group("level") == "INFO"
assert m3.group("logger") == "scheduler"
assert m3.group("message") == "job completed in 0.5s"
print("regex10 ✓")
