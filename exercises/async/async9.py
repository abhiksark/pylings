# Exercise: Async 9
# I AM NOT DONE
#
# Goal: Gather doubled values from several async calls.

import asyncio

async def double(value):
    await asyncio.sleep(0)
    return value * 2

async def double_all(values):
    return ???
