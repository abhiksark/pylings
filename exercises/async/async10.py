# Exercise: Async 10
# I AM NOT DONE
#
# Goal: Build a small async pipeline that fetches names and joins them.

import asyncio

async def fetch_name(name):
    await asyncio.sleep(0)
    return name.upper()

async def fetch_all(names):
    upper_names = ???
    return ",".join(upper_names)
