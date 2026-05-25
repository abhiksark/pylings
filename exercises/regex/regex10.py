# Exercise: Regex 10
# I AM NOT DONE
#
# Parse a structured log line and extract three fields:
#   level    — the log level word (e.g. "ERROR", "INFO", "WARNING")
#   logger   — the logger name (word characters only, e.g. "db.engine")
#   message  — everything after the colon+space at the end
#
# Log line format:
#   [LEVEL] logger_name: message text here
#
# Example:
#   "[ERROR] db.engine: connection refused"
#   → level="ERROR", logger="db.engine", message="connection refused"
#
# Use re.search with named capturing groups (?P<name>...).
# Fix the pattern (replace ???).
#
# Hints:
#   \[  and  \]   match literal square brackets
#   [\w.]+        matches word chars and dots (for dotted logger names)
#   .+            matches the rest of the line (message)

import re

log_line = "[ERROR] db.engine: connection refused"
pattern = "???"
match = re.search(pattern, log_line)
level = match.group("level")
logger = match.group("logger")
message = match.group("message")
