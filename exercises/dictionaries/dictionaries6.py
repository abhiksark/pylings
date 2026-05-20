# Exercise: Dictionaries 6
# I AM NOT DONE
#
# `.get(key, default)` returns the value for a key if it exists,
# or the default if the key is missing — without raising a KeyError.
#
# Given `config` below:
#   `timeout`  — get "timeout" with a default of 30
#   `retries`  — get "retries" with a default of 3
#   `verbose`  — get "verbose" with a default of False
#
# "timeout" exists in config, "retries" and "verbose" do not.

config = {"host": "localhost", "port": 8080, "timeout": 60}

timeout = ???
retries = ???
verbose = ???
