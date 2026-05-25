# Exercise: Async 6
# I AM NOT DONE
#
# Goal: Consume an async generator with async for.

async def numbers():
    for value in [1, 2, 3]:
        yield value

async def collect_numbers():
    result = []
    async for value in numbers():
        ???
    return result
