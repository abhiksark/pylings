import asyncio

assert asyncio.run(fetch_all(["ada", "lin", "guido"])) == "ADA,LIN,GUIDO"
print("async10 ok")
