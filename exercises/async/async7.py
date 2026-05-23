# Exercise: Async 7
# I AM NOT DONE
#
# Goal: Use asyncio.wait_for to apply a timeout to a coroutine.

import asyncio

async def quick():
    await asyncio.sleep(0)
    return "done"

async def with_timeout():
    return ???
