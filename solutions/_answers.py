from __future__ import annotations

import linecache
from pathlib import Path


ANSWERS: dict[str, str] = {'async1': 'async def greet():\n    return "hello async"\n',
 'async10': 'import asyncio\n'
            '\n'
            'async def fetch_name(name):\n'
            '    await asyncio.sleep(0)\n'
            '    return name.upper()\n'
            '\n'
            'async def fetch_all(names):\n'
            '    upper_names = await asyncio.gather(*(fetch_name(name) for name in names))\n'
            '    return ",".join(upper_names)\n',
 'async2': 'async def get_message():\n'
           '    return "ready"\n'
           '\n'
           'async def main():\n'
           '    return await get_message()\n',
 'async3': 'import asyncio\n'
           '\n'
           'async def wake_up():\n'
           '    await asyncio.sleep(0)\n'
           '    return "awake"\n',
 'async4': 'import asyncio\n'
           '\n'
           'async def first():\n'
           '    return "a"\n'
           '\n'
           'async def second():\n'
           '    return "b"\n'
           '\n'
           'async def collect():\n'
           '    return list(await asyncio.gather(first(), second()))\n',
 'async5': 'import asyncio\n'
           '\n'
           'async def compute():\n'
           '    return 21 * 2\n'
           '\n'
           'async def run_task():\n'
           '    task = asyncio.create_task(compute())\n'
           '    return await task\n',
 'async6': 'async def numbers():\n'
           '    for value in [1, 2, 3]:\n'
           '        yield value\n'
           '\n'
           'async def collect_numbers():\n'
           '    result = []\n'
           '    async for value in numbers():\n'
           '        result.append(value)\n'
           '    return result\n',
 'async7': 'import asyncio\n'
           '\n'
           'async def quick():\n'
           '    await asyncio.sleep(0)\n'
           '    return "done"\n'
           '\n'
           'async def with_timeout():\n'
           '    return await asyncio.wait_for(quick(), timeout=1)\n',
 'async8': 'import asyncio\n'
           '\n'
           'async def answer():\n'
           '    return 42\n'
           '\n'
           'result = asyncio.run(answer())\n',
 'async9': 'import asyncio\n'
           '\n'
           'async def double(value):\n'
           '    await asyncio.sleep(0)\n'
           '    return value * 2\n'
           '\n'
           'async def double_all(values):\n'
           '    return list(await asyncio.gather(*(double(value) for value in values)))\n',
 'classes1': 'class Cat:\n    pass\n\nmy_cat = Cat()\n',
 'classes10': 'class Circle:\n'
              '    pi = 3.14159\n'
              '\n'
              '    def __init__(self, radius):\n'
              '        self.radius = radius\n'
              '\n'
              '    def area(self):\n'
              '        return self.pi * self.radius ** 2\n'
              '\n'
              'c1 = Circle(1)\n'
              'c2 = Circle(5)\n',
 'classes11': 'class Temperature:\n'
              '    def __init__(self, degrees):\n'
              '        self.degrees = degrees\n'
              '\n'
              '    @classmethod\n'
              '    def from_string(cls, s):\n'
              '        return cls(float(s[:-1]))\n'
              '\n'
              't = Temperature.from_string("36.6C")\n'
              'boiling = Temperature.from_string("100C")\n',
 'classes12': 'class BankAccount:\n'
              '    def __init__(self, owner, balance):\n'
              '        self.owner = owner\n'
              '        self.balance = balance\n'
              '\n'
              '    def deposit(self, amount):\n'
              '        self.balance += amount\n'
              '\n'
              '    def withdraw(self, amount):\n'
              '        if amount > self.balance:\n'
              '            raise ValueError("insufficient funds")\n'
              '        self.balance -= amount\n'
              '\n'
              '    def __str__(self):\n'
              '        return f"BankAccount({self.owner}, balance={self.balance})"\n'
              '\n'
              'account = BankAccount("Alice", 100)\n'
              'account.deposit(50)\n'
              'account.withdraw(30)\n',
 'classes2': 'class Dog:\n'
             '    def __init__(self, name):\n'
             '        self.name = name\n'
             '\n'
             'rex = Dog("Rex")\n',
 'classes3': 'class Point:\n'
             '    def __init__(self, x, y):\n'
             '        self.x = x\n'
             '        self.y = y\n'
             '\n'
             'p = Point(3, 7)\n',
 'classes4': 'class Rectangle:\n'
             '    def __init__(self, width, height):\n'
             '        self.width = width\n'
             '        self.height = height\n'
             '\n'
             '    def area(self):\n'
             '        return self.width * self.height\n'
             '\n'
             'rect = Rectangle(4, 5)\n',
 'classes5': 'class Counter:\n'
             '    def __init__(self):\n'
             '        self.count = 0\n'
             '\n'
             '    def increment(self):\n'
             '        self.count += 1\n'
             '\n'
             'c = Counter()\n'
             'c.increment()\n'
             'c.increment()\n'
             'c.increment()\n',
 'classes6': 'class Car:\n'
             '    def __init__(self, brand, speed=0):\n'
             '        self.brand = brand\n'
             '        self.speed = speed\n'
             '\n'
             'slow = Car("Tesla")\n'
             'fast = Car("Ferrari", 200)\n',
 'classes7': 'class Greeter:\n'
             '    def __init__(self, name):\n'
             '        self.name = name\n'
             '\n'
             '    def get_name(self):\n'
             '        return self.name\n'
             '\n'
             '    def greet(self):\n'
             '        return f"Hello, {self.get_name()}!"\n'
             '\n'
             'g = Greeter("Alice")\n',
 'classes8': 'class Book:\n'
             '    def __init__(self, title, author):\n'
             '        self.title = title\n'
             '        self.author = author\n'
             '\n'
             '    def __str__(self):\n'
             '        return f"Book: {self.title} by {self.author}"\n'
             '\n'
             'book = Book("1984", "Orwell")\n',
 'classes9': 'class Color:\n'
             '    def __init__(self, r, g, b):\n'
             '        self.r = r\n'
             '        self.g = g\n'
             '        self.b = b\n'
             '\n'
             '    def __str__(self):\n'
             '        return f"rgb({self.r}, {self.g}, {self.b})"\n'
             '\n'
             '    def __repr__(self):\n'
             '        return f"Color(r={self.r}, g={self.g}, b={self.b})"\n'
             '\n'
             'c = Color(255, 128, 0)\n',
 'collections1': 'from collections import Counter\n'
                 'words = ["apple", "banana", "apple", "cherry", "banana", "apple"]\n'
                 'counts = Counter(words)\n',
 'collections10': 'from collections import Counter, defaultdict\n'
                  'log = [("api",120), ("web",45), ("api",95), ("db",300), ("web",60), '
                  '("api",110), ("db",280), ("web",55), ("api",85), ("db",310), ("web",50), '
                  '("api",100)]\n'
                  'grouped = defaultdict(list)\n'
                  'for category, value in log:\n'
                  '    grouped[category].append(value)\n'
                  'hit_counts = Counter(category for category, _ in log)\n'
                  'top_category = hit_counts.most_common(1)[0][0]\n'
                  'avg_times = {category: sum(values) / len(values) for category, values in '
                  'grouped.items()}\n',
 'collections2': 'from collections import Counter\n'
                 'votes = ["Alice", "Bob", "Alice", "Carol", "Bob", "Alice", "Carol", "Bob", '
                 '"Alice", "Carol"]\n'
                 'tally = Counter(votes)\n'
                 'top2 = tally.most_common(2)\n',
 'collections3': 'from collections import defaultdict\n'
                 'text = "mississippi"\n'
                 'char_counts = defaultdict(int)\n'
                 'for ch in text:\n'
                 '    char_counts[ch] += 1\n',
 'collections4': 'from collections import defaultdict\n'
                 'students = [("Alice", "A"), ("Bob", "B"), ("Carol", "A"), ("Dave", "C"), ("Eve", '
                 '"B"), ("Frank", "A")]\n'
                 'by_grade = defaultdict(list)\n'
                 'for name, grade in students:\n'
                 '    by_grade[grade].append(name)\n',
 'collections5': 'from collections import namedtuple\n'
                 'Point = namedtuple("Point", ["x", "y"])\n'
                 'p = Point(3, 4)\n',
 'collections6': 'from collections import namedtuple\n'
                 'Card = namedtuple("Card", ["rank", "suit"])\n'
                 'card = Card("K", "spades")\n'
                 'upgraded = card._replace(rank="A")\n',
 'collections7': 'from collections import deque\n'
                 'd = deque()\n'
                 'd.appendleft(1)\n'
                 'd.append(2)\n'
                 'd.appendleft(0)\n'
                 'right_val = d.pop()\n'
                 'left_val = d.popleft()\n',
 'collections8': 'from collections import deque\n'
                 'queue = deque()\n'
                 'queue.append("doc1")\n'
                 'queue.append("doc2")\n'
                 'queue.append("doc3")\n'
                 'first = queue.popleft()\n'
                 'second = queue.popleft()\n'
                 'third = queue.popleft()\n',
 'collections9': 'from collections import Counter\n'
                 'monday = Counter({"apple": 5, "banana": 3, "cherry": 2})\n'
                 'tuesday = Counter({"apple": 2, "banana": 4, "date": 1})\n'
                 'sold = Counter({"apple": 4, "banana": 5, "cherry": 1})\n'
                 'combined = monday + tuesday\n'
                 'remainder = combined - sold\n',
 'comprehensions1': 'numbers = [x for x in range(5)]\n',
 'comprehensions10': 'words = ["apple", "banana", "cherry", "date"]\n'
                     'word_index = {word: idx for idx, word in enumerate(words)}\n',
 'comprehensions2': 'values = [1, 2, 3, 4, 5, 6, 7, 8]\n'
                    'evens = [x for x in values if x % 2 == 0]\n',
 'comprehensions3': 'values = [1, 2, 3, 4, 5]\ndoubled = [x * 2 for x in values]\n',
 'comprehensions4': 'rows = [0, 1]\n'
                    'cols = [0, 1, 2]\n'
                    'pairs = [(row, col) for row in rows for col in cols]\n',
 'comprehensions5': 'numbers = [1, 2, 3, 4, 5]\nsquared = {n: n * n for n in numbers}\n',
 'comprehensions6': 'words = ["apple", "bat", "car", "dog", "elephant", "fig"]\n'
                    'unique_lengths = {len(word) for word in words}\n',
 'comprehensions7': 'sentence = "list comprehensions are quite powerful"\n'
                    'vowels = [c for c in sentence if c in "aeiou"]\n',
 'comprehensions8': 'values = [1, 2, 3, 4, 5, 6]\n'
                    'labels = ["even" if x % 2 == 0 else "odd" for x in values]\n',
 'comprehensions9': 'matrix = [[1,2,3], [4,5,6], [7,8,9]]\n'
                    'flat = [item for row in matrix for item in row]\n',
 'conditionals1': 'is_sunny = True\n'
                  'message = ""\n'
                  'if is_sunny:\n'
                  '    message = "Let\'s go outside!"\n',
 'conditionals10': 'def classify(n):\n'
                   '    if n > 100:\n'
                   '        return "large positive"\n'
                   '    elif n > 0:\n'
                   '        return "small positive"\n'
                   '    elif n == 0:\n'
                   '        return "zero"\n'
                   '    elif n >= -100:\n'
                   '        return "small negative"\n'
                   '    return "large negative"\n',
 'conditionals2': 'def sign(n):\n'
                  '    if n > 0:\n'
                  '        return "positive"\n'
                  '    return "non-positive"\n',
 'conditionals3': 'def grade(score):\n'
                  '    if score >= 90:\n'
                  '        return "A"\n'
                  '    elif score >= 80:\n'
                  '        return "B"\n'
                  '    elif score >= 70:\n'
                  '        return "C"\n'
                  '    return "F"\n',
 'conditionals4': 'def compare(a, b):\n'
                  '    if a < b:\n'
                  '        return "less"\n'
                  '    elif a == b:\n'
                  '        return "equal"\n'
                  '    return "greater"\n',
 'conditionals5': 'def can_ride(height, has_ticket):\n'
                  '    return height >= 120 and has_ticket\n'
                  '\n'
                  'def gets_discount(is_student, is_senior):\n'
                  '    return is_student or is_senior\n',
 'conditionals6': 'def is_closed(is_open):\n'
                  '    return not is_open\n'
                  '\n'
                  'def neither_zero(a, b):\n'
                  '    return not (a == 0 or b == 0)\n',
 'conditionals7': 'def ticket_price(age, is_member):\n'
                  '    if age < 5:\n'
                  '        return 0\n'
                  '    else:\n'
                  '        if is_member:\n'
                  '            return 8\n'
                  '        return 12\n',
 'conditionals8': 'def describe(value):\n'
                  '    if value:\n'
                  '        return "has content"\n'
                  '    return "empty"\n',
 'conditionals9': 'def absolute(n):\n    return n if n >= 0 else -n\n',
 'context_managers1': 'import tempfile\n'
                      'data_path = tempfile.mktemp()\n'
                      'with open(data_path, "w") as f:\n'
                      '    f.write("hello, context!")\n',
 'context_managers2': 'import tempfile\n'
                      'data_path = tempfile.mktemp()\n'
                      'with open(data_path, "w") as f:\n'
                      '    f.write("closed check")\n',
 'context_managers3': 'class Timer:\n'
                      '    def __init__(self):\n'
                      '        self.finished = False\n'
                      '\n'
                      '    def __enter__(self):\n'
                      '        return self\n'
                      '\n'
                      '    def __exit__(self, exc_type, exc_val, exc_tb):\n'
                      '        self.finished = True\n'
                      '\n'
                      't = Timer()\n'
                      'with t:\n'
                      '    pass\n',
 'context_managers4': 'class ManagedList:\n'
                      '    def __init__(self):\n'
                      '        self.items = []\n'
                      '        self.log = []\n'
                      '\n'
                      '    def __enter__(self):\n'
                      '        return self\n'
                      '\n'
                      '    def __exit__(self, exc_type, exc_val, exc_tb):\n'
                      '        self.log.append("done")\n'
                      '\n'
                      'ml = ManagedList()\n'
                      'with ml as resource:\n'
                      '    resource.items.append(1)\n'
                      '    resource.items.append(2)\n',
 'context_managers5': 'class DatabaseConnection:\n'
                      '    def __init__(self, dsn):\n'
                      '        self.dsn = dsn\n'
                      '        self.open = True\n'
                      '        self.connection = {"dsn": dsn, "active": True}\n'
                      '\n'
                      '    def __enter__(self):\n'
                      '        return self.connection\n'
                      '\n'
                      '    def __exit__(self, exc_type, exc_val, exc_tb):\n'
                      '        self.open = False\n'
                      '\n'
                      'db = DatabaseConnection("sqlite:///:memory:")\n'
                      'with db as conn:\n'
                      '    result = conn\n',
 'context_managers6': 'from contextlib import contextmanager\n'
                      '\n'
                      '@contextmanager\n'
                      'def managed_counter():\n'
                      '    counter = []\n'
                      '    try:\n'
                      '        yield counter\n'
                      '    finally:\n'
                      '        counter.append("finished")\n'
                      '\n'
                      'with managed_counter() as counter:\n'
                      '    counter.append(1)\n'
                      '    counter.append(2)\n',
 'context_managers7': 'class SilentZeroDivision:\n'
                      '    def __enter__(self):\n'
                      '        return self\n'
                      '\n'
                      '    def __exit__(self, exc_type, exc_val, exc_tb):\n'
                      '        if exc_type is ZeroDivisionError:\n'
                      '            return True\n'
                      '        return None\n'
                      '\n'
                      'result = "not set"\n'
                      'with SilentZeroDivision():\n'
                      '    result = 1 / 0\n'
                      '    result = "unreachable"\n',
 'context_managers8': 'from contextlib import contextmanager\n'
                      '\n'
                      'class Resource:\n'
                      '    def __init__(self):\n'
                      '        self.acquired = False\n'
                      '        self.release_log = []\n'
                      '\n'
                      '    def __enter__(self):\n'
                      '        self.acquired = True\n'
                      '        return self\n'
                      '\n'
                      '    def __exit__(self, exc_type, exc_val, exc_tb):\n'
                      '        self.acquired = False\n'
                      '        self.release_log.append("released")\n'
                      '\n'
                      '@contextmanager\n'
                      'def ManagedPool(resource):\n'
                      '    resource.__enter__()\n'
                      '    try:\n'
                      '        yield resource\n'
                      '    finally:\n'
                      '        resource.__exit__(None, None, None)\n'
                      '\n'
                      'r = Resource()\n'
                      'with ManagedPool(r) as res:\n'
                      '    in_block_acquired = res.acquired\n',
 'dataclasses1': 'from dataclasses import dataclass\n'
                 '\n'
                 '@dataclass\n'
                 'class Point:\n'
                 '    x: int\n'
                 '    y: int\n'
                 '\n'
                 'origin = Point(0, 0)\n',
 'dataclasses2': 'from dataclasses import dataclass\n'
                 '\n'
                 '@dataclass\n'
                 'class Color:\n'
                 '    red: int\n'
                 '    green: int\n'
                 '    blue: int\n'
                 '\n'
                 'orange = Color(255, 128, 0)\n'
                 'description = f"R={orange.red} G={orange.green} B={orange.blue}"\n',
 'dataclasses3': 'from dataclasses import dataclass\n'
                 '\n'
                 '@dataclass\n'
                 'class Measurement:\n'
                 '    value: float\n'
                 '    unit: str = "m/s\\u00b2"\n'
                 '\n'
                 'gravity = Measurement(9.8)\n'
                 'named = Measurement(100.0, "km/h")\n',
 'dataclasses4': 'from dataclasses import dataclass, field\n'
                 '\n'
                 '@dataclass\n'
                 'class Basket:\n'
                 '    label: str\n'
                 '    items: list = field(default_factory=list)\n'
                 '\n'
                 'b1 = Basket("fruit")\n'
                 'b2 = Basket("veggies")\n'
                 'b1.items.append("apple")\n',
 'dataclasses5': 'from dataclasses import dataclass\n'
                 '\n'
                 '@dataclass\n'
                 'class Vector3:\n'
                 '    x: float\n'
                 '    y: float\n'
                 '    z: float\n'
                 '\n'
                 'v = Vector3(1.0, 2.0, 3.0)\n',
 'dataclasses6': 'from dataclasses import dataclass\n'
                 '\n'
                 '@dataclass\n'
                 'class Book:\n'
                 '    title: str\n'
                 '    pages: int\n'
                 '\n'
                 'novel = Book("Dune", 412)\n'
                 'copy = Book("Dune", 412)\n'
                 'other = Book("Foundation", 255)\n',
 'dataclasses7': 'from dataclasses import dataclass\n'
                 '\n'
                 '@dataclass(frozen=True)\n'
                 'class Config:\n'
                 '    host: str\n'
                 '    port: int\n'
                 '\n'
                 'cfg = Config("localhost", 8080)\n'
                 'try:\n'
                 '    cfg.port = 9090\n'
                 '    mutation_raised = False\n'
                 'except Exception:\n'
                 '    mutation_raised = True\n',
 'dataclasses8': 'from dataclasses import dataclass\n'
                 '\n'
                 '@dataclass\n'
                 'class Rectangle:\n'
                 '    width: float\n'
                 '    height: float\n'
                 '\n'
                 '    def area(self) -> float:\n'
                 '        return self.width * self.height\n'
                 '\n'
                 '    def perimeter(self) -> float:\n'
                 '        return 2 * (self.width + self.height)\n'
                 '\n'
                 'rect = Rectangle(4.0, 3.0)\n'
                 'square = Rectangle(5.0, 5.0)\n',
 'datetime1': 'from datetime import date\nlaunch_day = date(2026, 5, 23)\n',
 'datetime2': 'from datetime import date, timedelta\n'
              'start = date(2026, 5, 23)\n'
              'next_week = start + timedelta(days=7)\n',
 'datetime3': 'from datetime import datetime\n'
              'raw = "2026-05-23 09:30"\n'
              'meeting = datetime.strptime(raw, "%Y-%m-%d %H:%M")\n',
 'datetime4': 'from datetime import date\n'
              'day = date(2026, 5, 23)\n'
              'formatted = day.strftime("%d/%m/%Y")\n',
 'datetime5': 'from datetime import date\n'
              'today = date(2026, 5, 23)\n'
              'due = date(2026, 6, 1)\n'
              'is_future = due > today\n',
 'datetime6': 'from datetime import date\n'
              'start = date(2026, 5, 1)\n'
              'end = date(2026, 5, 23)\n'
              'days_between = (end - start).days\n',
 'datetime7': 'from datetime import date, datetime, time\n'
              'day = date(2026, 5, 23)\n'
              'clock = time(14, 45)\n'
              'appointment = datetime.combine(day, clock)\n',
 'datetime8': 'from datetime import date\n'
              'raw_dates = ["2026-05-23", "2024-01-01", "2025-12-31"]\n'
              'parsed = [date.fromisoformat(value) for value in raw_dates]\n'
              'earliest = min(parsed)\n'
              'latest = max(parsed)\n',
 'decorators1': 'def call_it(func):\n'
                '    return func()\n'
                '\n'
                'def say_hello():\n'
                '    return "hello"\n'
                '\n'
                'def give_seven():\n'
                '    return 7\n',
 'decorators10': 'import functools\n'
                 '\n'
                 'def memoize(func):\n'
                 '    @functools.wraps(func)\n'
                 '    def wrapper(*args):\n'
                 '        if args not in wrapper.cache:\n'
                 '            wrapper.cache[args] = func(*args)\n'
                 '        return wrapper.cache[args]\n'
                 '    wrapper.cache = {}\n'
                 '    return wrapper\n'
                 '\n'
                 'call_count = 0\n'
                 '\n'
                 '@memoize\n'
                 'def slow_square(n):\n'
                 '    global call_count\n'
                 '    call_count += 1\n'
                 '    return n * n\n',
 'decorators2': 'def shout(func):\n'
                '    def wrapper():\n'
                '        result = func()\n'
                '        return result.upper()\n'
                '    return wrapper\n'
                '\n'
                'def greet():\n'
                '    return "hello"\n'
                '\n'
                'loud_greet = shout(greet)\n',
 'decorators3': 'def stamp(func):\n'
                '    def wrapper():\n'
                '        return "[STAMPED] " + func()\n'
                '    return wrapper\n'
                '\n'
                '@stamp\n'
                'def get_message():\n'
                '    return "hello"\n',
 'decorators4': 'def double_result(func):\n'
                '    def wrapper():\n'
                '        return func() * 2\n'
                '    return wrapper\n'
                '\n'
                '@double_result\n'
                'def get_five():\n'
                '    return 5\n'
                '\n'
                '@double_result\n'
                'def get_ten():\n'
                '    return 10\n',
 'decorators5': 'def log_call(func):\n'
                '    def wrapper(*args, **kwargs):\n'
                '        print(f"calling {func.__name__}")\n'
                '        return func(*args, **kwargs)\n'
                '    return wrapper\n'
                '\n'
                '@log_call\n'
                'def add(a, b):\n'
                '    return a + b\n'
                '\n'
                '@log_call\n'
                'def greet(name, greeting="Hello"):\n'
                '    return f"{greeting}, {name}!"\n',
 'decorators6': 'import functools\n'
                '\n'
                'def preserve(func):\n'
                '    @functools.wraps(func)\n'
                '    def wrapper(*args, **kwargs):\n'
                '        return func(*args, **kwargs)\n'
                '    return wrapper\n'
                '\n'
                '@preserve\n'
                'def compute(x, y):\n'
                '    """Return the sum of x and y."""\n'
                '    return x + y\n',
 'decorators7': 'import functools\n'
                '\n'
                'def count_calls(func):\n'
                '    @functools.wraps(func)\n'
                '    def wrapper(*args, **kwargs):\n'
                '        wrapper.call_count += 1\n'
                '        return func(*args, **kwargs)\n'
                '    wrapper.call_count = 0\n'
                '    return wrapper\n'
                '\n'
                '@count_calls\n'
                'def add(a, b):\n'
                '    return a + b\n',
 'decorators8': 'import functools\n'
                '\n'
                'def repeat(n):\n'
                '    def decorator(func):\n'
                '        @functools.wraps(func)\n'
                '        def wrapper(*args, **kwargs):\n'
                '            result = None\n'
                '            for _ in range(n):\n'
                '                result = func(*args, **kwargs)\n'
                '            return result\n'
                '        return wrapper\n'
                '    return decorator\n'
                '\n'
                '@repeat(3)\n'
                'def say(word):\n'
                '    return word\n'
                '\n'
                '@repeat(1)\n'
                'def identity(x):\n'
                '    return x\n',
 'decorators9': 'def add_a(func):\n'
                '    def wrapper():\n'
                '        return "[A]" + func()\n'
                '    return wrapper\n'
                '\n'
                'def add_b(func):\n'
                '    def wrapper():\n'
                '        return "[B]" + func()\n'
                '    return wrapper\n'
                '\n'
                '@add_b\n'
                '@add_a\n'
                'def get_value():\n'
                '    return "42"\n',
 'dictionaries1': 'ages = {"alice": 30, "bob": 25}\n',
 'dictionaries10': 'words = ["the", "cat", "sat", "on", "the", "mat", "and", "the", "cat", "hat"]\n'
                   'freq = {}\n'
                   'for word in words:\n'
                   '    freq[word] = freq.get(word, 0) + 1\n',
 'dictionaries2': 'capitals = {"france": "Paris", "germany": "Berlin", "japan": "Tokyo"}\n'
                  'france_capital = capitals["france"]\n',
 'dictionaries3': 'scores = {"alice": 75, "bob": 60, "carol": 82}\n'
                  'scores["diana"] = 91\n'
                  'scores["alice"] = 88\n',
 'dictionaries4': 'basket = {"apple": 5, "banana": 3, "cherry": 12, "date": 7}\n'
                  'del basket["banana"]\n'
                  'cherry_count = basket.pop("cherry")\n',
 'dictionaries5': 'inventory = {"pen": 10, "notebook": 5, "eraser": 8}\n'
                  'all_items = list(inventory.keys())\n'
                  'all_counts = list(inventory.values())\n'
                  'all_pairs = list(inventory.items())\n',
 'dictionaries6': 'config = {"host": "localhost", "port": 8080, "timeout": 60}\n'
                  'timeout = config.get("timeout", 30)\n'
                  'retries = config.get("retries", 3)\n'
                  'verbose = config.get("verbose", False)\n',
 'dictionaries7': 'prices = {"apple": 1.0, "milk": 1.5, "bread": 2.5}\n'
                  'discounted = {}\n'
                  'for item, price in prices.items():\n'
                  '    discounted[item] = round(price * 0.9, 2)\n',
 'dictionaries8': 'permissions = {"read": True, "write": False}\n'
                  'can_read = "read" in permissions\n'
                  'can_write = "write" in permissions\n'
                  'can_delete = "delete" in permissions\n',
 'dictionaries9': 'school = {\n'
                  '    "students": {"alice": {"grade": "A", "age": 20}, "bob": {"grade": "B", '
                  '"age": 22}},\n'
                  '    "courses": {"math": {"room": 101, "credits": 3}, "english": {"room": 205, '
                  '"credits": 3}},\n'
                  '    "meta": {"enrollment": 350, "founded": 1990},\n'
                  '}\n'
                  'alice_grade = school["students"]["alice"]["grade"]\n'
                  'math_room = school["courses"]["math"]["room"]\n'
                  'num_students = school["meta"]["enrollment"]\n',
 'enums1': 'from enum import Enum\n'
           '\n'
           'class Color(Enum):\n'
           '    RED = "red"\n'
           '    BLUE = "blue"\n'
           '\n'
           'favorite = Color.RED\n',
 'enums2': 'from enum import Enum, auto\n'
           '\n'
           'class Status(Enum):\n'
           '    TODO = 1\n'
           '    DOING = 2\n'
           '    DONE = 3\n',
 'enums3': 'from enum import Enum\n'
           '\n'
           'class Priority(Enum):\n'
           '    LOW = 1\n'
           '    MEDIUM = 3\n'
           '    HIGH = 5\n'
           '\n'
           'selected = Priority.HIGH\n'
           'selected_name = selected.name\n'
           'selected_value = selected.value\n',
 'enums4': 'from enum import Enum\n'
           '\n'
           'class Size(Enum):\n'
           '    SMALL = "S"\n'
           '    MEDIUM = "M"\n'
           '    LARGE = "L"\n'
           '\n'
           'size_codes = [size.value for size in Size]\n',
 'enums5': 'from enum import Enum, auto\n'
           '\n'
           'class TicketState(Enum):\n'
           '    OPEN = auto()\n'
           '    CLOSED = auto()\n'
           '    CANCELLED = auto()\n'
           '\n'
           'def is_terminal(state):\n'
           '    return state in {TicketState.CLOSED, TicketState.CANCELLED}\n',
 'enums6': 'from enum import Enum\n'
           '\n'
           'class Direction(Enum):\n'
           '    NORTH = (0, -1)\n'
           '    SOUTH = (0, 1)\n'
           '    EAST = (1, 0)\n'
           '    WEST = (-1, 0)\n'
           '\n'
           '    def delta(self):\n'
           '        return self.value\n',
 'exceptions1': 'def safe_divide(a, b):\n'
                '    try:\n'
                '        return a / b\n'
                '    except ZeroDivisionError:\n'
                '        return "error"\n',
 'exceptions10': 'def validate_username(name):\n'
                 '    if not isinstance(name, str):\n'
                 '        raise TypeError("username must be a str")\n'
                 '    if len(name) < 3 or len(name) > 20:\n'
                 '        raise ValueError("username must be 3-20 characters")\n'
                 '    if not name.isalnum():\n'
                 '        raise ValueError("username must be alphanumeric")\n'
                 '    return name.lower()\n',
 'exceptions2': 'def parse_number(s):\n'
                '    try:\n'
                '        return int(s)\n'
                '    except ValueError:\n'
                '        return -1\n',
 'exceptions3': 'def describe_error(s):\n'
                '    try:\n'
                '        return float(s)\n'
                '    except ValueError as e:\n'
                '        return str(e)\n',
 'exceptions4': 'def load_value(data, key):\n'
                '    try:\n'
                '        value = data[key]\n'
                '    except KeyError:\n'
                '        return "missing"\n'
                '    else:\n'
                '        return value * 2\n',
 'exceptions5': 'log = []\n'
                '\n'
                'def read_first(items):\n'
                '    try:\n'
                '        return items[0]\n'
                '    except IndexError:\n'
                '        return None\n'
                '    finally:\n'
                '        log.append("done")\n',
 'exceptions6': 'def require_positive(n):\n'
                '    if n <= 0:\n'
                '        raise ValueError\n'
                '    return n\n',
 'exceptions7': 'def check_age(age):\n'
                '    if age < 0 or age > 120:\n'
                '        raise ValueError("age must be between 0 and 120")\n'
                '    return age\n',
 'exceptions8': 'def classify_error(func):\n'
                '    try:\n'
                '        func()\n'
                '        return "ok"\n'
                '    except ValueError:\n'
                '        return "value error"\n'
                '    except TypeError:\n'
                '        return "type error"\n'
                '    except Exception:\n'
                '        return "other error"\n',
 'exceptions9': 'class InsufficientFundsError(Exception):\n'
                '    pass\n'
                '\n'
                'def withdraw(balance, amount):\n'
                '    if amount > balance:\n'
                '        raise InsufficientFundsError(f"cannot withdraw {amount} from balance of '
                '{balance}")\n'
                '    return balance - amount\n',
 'file_io1': 'import tempfile\n'
             'data_path = tempfile.mktemp()\n'
             'with open(data_path, "w") as f:\n'
             '    f.write("hello, file!")\n',
 'file_io10': 'import tempfile\n'
              'src_path = tempfile.mktemp()\n'
              'dst_path = tempfile.mktemp()\n'
              'with open(src_path, "w") as f:\n'
              '    f.write("hello world\\npython is fun\\nfile io rocks\\n")\n'
              'with open(src_path) as src:\n'
              '    with open(dst_path, "w") as dst:\n'
              '        for line in src:\n'
              '            dst.write(line.upper())\n',
 'file_io2': 'import tempfile\n'
             'note_path = tempfile.mktemp()\n'
             'with open(note_path, "w") as f:\n'
             '    f.write("remember")\n'
             'with open(note_path) as f:\n'
             '    contents = f.read()\n',
 'file_io3': 'import tempfile\n'
             'log_path = tempfile.mktemp()\n'
             'with open(log_path, "w") as fh:\n'
             '    fh.write("first entry")\n',
 'file_io4': 'import tempfile\n'
             'poem_path = tempfile.mktemp()\n'
             'with open(poem_path, "w") as f:\n'
             '    f.write("roses are red\\nviolets are blue\\npython is great\\n")\n'
             'with open(poem_path) as f:\n'
             '    lines = f.readlines()\n',
 'file_io5': 'import tempfile\n'
             'journal_path = tempfile.mktemp()\n'
             'with open(journal_path, "w") as f:\n'
             '    f.write("day 1: sunny\\n")\n'
             'with open(journal_path, "a") as fh:\n'
             '    fh.write("day 2: rainy\\n")\n',
 'file_io6': 'import tempfile\n'
             'numbers_path = tempfile.mktemp()\n'
             'with open(numbers_path, "w") as f:\n'
             '    f.write("10\\n20\\n30\\n40\\n50\\n")\n'
             'total = 0\n'
             'with open(numbers_path) as fh:\n'
             '    for line in fh:\n'
             '        total += int(line.strip())\n',
 'file_io7': 'import tempfile\n'
             'words_path = tempfile.mktemp()\n'
             'words = ["alpha", "beta", "gamma"]\n'
             'with open(words_path, "w") as fh:\n'
             '    for word in words:\n'
             '        fh.write(word + "\\n")\n',
 'file_io8': 'import tempfile\n'
             'source_path = tempfile.mktemp()\n'
             'with open(source_path, "w") as f:\n'
             '    f.write("  Hello, World!  ")\n'
             'with open(source_path) as fh:\n'
             '    result = fh.read().strip()\n',
 'file_io9': 'import tempfile\n'
             'essay_path = tempfile.mktemp()\n'
             'with open(essay_path, "w") as f:\n'
             '    f.write("the quick brown fox jumps over the lazy dog")\n'
             'with open(essay_path) as fh:\n'
             '    word_count = len(fh.read().split())\n',
 'functional1': 'square = lambda x: x * x\n',
 'functional10': 'from functools import reduce\n'
                 'scores = [1, 3, 6, 2, 8, 4]\n'
                 'doubled = list(map(lambda x: x * 2, scores))\n'
                 'above_ten = list(filter(lambda x: x > 10, doubled))\n'
                 'result = reduce(lambda a, b: a + b, above_ten)\n',
 'functional2': 'absolute = lambda x: x if x >= 0 else -x\n',
 'functional3': 'numbers = [1, 2, 3, 4, 5]\ndoubled = list(map(lambda x: x * 2, numbers))\n',
 'functional4': 'numbers = [1,2,3,4,5,6,7,8,9,10]\n'
                'evens = list(filter(lambda x: x % 2 == 0, numbers))\n',
 'functional5': 'words = ["banana", "fig", "apple", "kiwi", "date"]\n'
                'by_length = sorted(words, key=lambda word: len(word))\n',
 'functional6': 'def apply_twice(func, value):\n'
                '    return func(func(value))\n'
                '\n'
                'triple = lambda x: x * 3\n'
                'add_ten = lambda x: x + 10\n',
 'functional7': 'def make_multiplier(n):\n    return lambda x: x * n\n',
 'functional8': 'from functools import reduce\n'
                'numbers = [1, 2, 3, 4, 5]\n'
                'product = reduce(lambda a, b: a * b, numbers)\n',
 'functional9': 'numbers = [3, -1, 4, 1, 5]\n'
                'positives = [2, 7, 11, 5]\n'
                'has_negative = any(x < 0 for x in numbers)\n'
                'all_positive = all(x > 0 for x in positives)\n',
 'functions1': 'def average(a, b):\n    return (a + b) / 2\n',
 'functions10': 'words = ["racecar", "hello", "level", "world", "madam", "python", "noon"]\n'
                '\n'
                'def is_palindrome(s):\n'
                '    s = s.lower()\n'
                '    return s == s[::-1]\n'
                '\n'
                'palindromes = [w for w in words if is_palindrome(w)]\n',
 'functions2': 'def greet():\n    return "hello"\n\nmessage = greet()\n',
 'functions3': 'def double(n):\n    return n * 2\n',
 'functions4': 'def square(n):\n    return n * n\n',
 'functions5': 'def make_greeting(name, greeting="Hello"):\n    return f"{greeting}, {name}!"\n',
 'functions6': 'def describe_pet(name, animal_type):\n'
               '    return f"My {animal_type} is named {name}."\n'
               '\n'
               'description = describe_pet(animal_type="dog", name="Buddy")\n',
 'functions7': 'def total(*args):\n    return sum(args)\n',
 'functions8': 'def build_profile(**kwargs):\n    return dict(kwargs)\n',
 'functions9': 'numbers = [3, 1, 4, 1, 5, 9, 2, 6]\n'
               '\n'
               'def min_max(nums):\n'
               '    return min(nums), max(nums)\n'
               '\n'
               'lo, hi = min_max(numbers)\n',
 'generators1': 'def count_up_to(n):\n    for i in range(1, n + 1):\n        yield i\n',
 'generators10': 'def running_total(numbers):\n'
                 '    total = 0\n'
                 '    for n in numbers:\n'
                 '        total += n\n'
                 '        yield total\n',
 'generators2': 'def squares(n):\n'
                '    for i in range(1, n + 1):\n'
                '        yield i * i\n'
                '\n'
                'result = list(squares(5))\n',
 'generators3': 'def evens_up_to(n):\n'
                '    for i in range(1, n + 1):\n'
                '        if i % 2 == 0:\n'
                '            yield i\n'
                '\n'
                'collected = []\n'
                'for value in evens_up_to(8):\n'
                '    collected.append(value)\n',
 'generators4': 'cube_gen = (i ** 3 for i in range(1, 6))\n',
 'generators5': 'def letters():\n'
                '    yield "a"\n'
                '    yield "b"\n'
                '    yield "c"\n'
                '\n'
                'gen = letters()\n'
                'first = next(gen)\n'
                'second = next(gen)\n'
                'third = next(gen)\n',
 'generators6': 'import itertools\n'
                '\n'
                'def natural_numbers():\n'
                '    n = 1\n'
                '    while True:\n'
                '        yield n\n'
                '        n += 1\n'
                '\n'
                'first_ten = list(itertools.islice(natural_numbers(), 10))\n',
 'generators7': 'def fibonacci():\n'
                '    a, b = 0, 1\n'
                '    while True:\n'
                '        yield a\n'
                '        a, b = b, a + b\n',
 'generators8': 'class Countdown:\n'
                '    def __init__(self, start):\n'
                '        self.start = start\n'
                '\n'
                '    def __iter__(self):\n'
                '        for value in range(self.start, 0, -1):\n'
                '            yield value\n',
 'generators9': 'class Counter:\n'
                '    def __init__(self, stop):\n'
                '        self.stop = stop\n'
                '        self.current = 0\n'
                '\n'
                '    def __iter__(self):\n'
                '        return self\n'
                '\n'
                '    def __next__(self):\n'
                '        if self.current >= self.stop:\n'
                '            raise StopIteration\n'
                '        value = self.current\n'
                '        self.current += 1\n'
                '        return value\n',
 'itertools1': 'from itertools import chain\n'
               'letters = ["a", "b"]\n'
               'numbers = [1, 2, 3]\n'
               'combined = list(chain(letters, numbers))\n',
 'itertools2': 'from itertools import count, islice\nfirst_four = list(islice(count(10), 4))\n',
 'itertools3': 'from itertools import product\n'
               'xs = [0, 1]\n'
               'ys = ["low", "high"]\n'
               'coordinates = list(product(xs, ys))\n',
 'itertools4': 'from itertools import groupby\n'
               'rows = [("fruit", "apple"), ("fruit", "pear"), ("veg", "carrot")]\n'
               'grouped = {category: [name for _, name in group] for category, group in '
               'groupby(rows, key=lambda row: row[0])}\n',
 'itertools5': 'from itertools import accumulate\n'
               'values = [3, 4, 5, 6]\n'
               'running_totals = list(accumulate(values))\n',
 'itertools6': 'from itertools import cycle, islice\n'
               'colors = ["red", "blue"]\n'
               'repeated = list(islice(cycle(colors), 6))\n',
 'itertools7': 'from itertools import zip_longest\n'
               'left = ["a", "b", "c"]\n'
               'right = [1]\n'
               'pairs = list(zip_longest(left, right, fillvalue="?"))\n',
 'itertools8': 'from itertools import pairwise\n'
               'batches = [[1, 2], [3], [4, 5]]\n'
               'flattened = [item for batch in batches for item in batch]\n'
               'adjacent_pairs = list(pairwise(flattened))\n',
 'json1': 'import json\n'
          'raw = \'{"name": "Ada", "language": "Python"}\'\n'
          'data = json.loads(raw)\n'
          'name = data["name"]\n',
 'json2': 'import json\npayload = {"b": 2, "a": 1}\ntext = json.dumps(payload, sort_keys=True)\n',
 'json3': 'import json\n'
          'raw = \'{"user": {"name": "Grace", "address": {"city": "London"}}}\'\n'
          'profile = json.loads(raw)\n'
          'city = profile["user"]["address"]["city"]\n',
 'json4': 'import io\n'
          'import json\n'
          'payload = {"ok": True, "count": 3}\n'
          'buffer = io.StringIO()\n'
          'json.dump(payload, buffer)\n'
          'buffer.seek(0)\n'
          'restored = json.load(buffer)\n',
 'json5': 'import json\n'
          'data = json.loads(\'{"name": "Pylings"}\')\n'
          'timezone = data.get("timezone", "UTC")\n',
 'json6': 'import json\n'
          'raw = \'[{"name": "Ada", "active": true}, {"name": "Lin", "active": false}, {"name": '
          '"Guido", "active": true}]\'\n'
          'users = json.loads(raw)\n'
          'active_names = [user["name"] for user in users if user["active"]]\n',
 'json7': 'import json\n'
          'settings = json.loads(\'{"theme": "light", "font_size": 12}\')\n'
          'settings["theme"] = "dark"\n'
          'encoded = json.dumps(settings, sort_keys=True)\n',
 'json8': 'import json\n'
          'original = {"project": "pylings", "tags": ["python", "practice"], "meta": {"level": '
          '3}}\n'
          'encoded = json.dumps(original, sort_keys=True)\n'
          'decoded = json.loads(encoded)\n'
          'tag_count = len(decoded["tags"])\n'
          'level = decoded["meta"]["level"]\n',
 'lists1': 'colors = ["red", "green", "blue"]\n',
 'lists10': 'sales = [\n'
            '    {"product": "apple", "units": 5, "price_per_unit": 1.20},\n'
            '    {"product": "banana", "units": 15, "price_per_unit": 18.0},\n'
            '    {"product": "cherry", "units": 8, "price_per_unit": 3.50},\n'
            '    {"product": "date", "units": 20, "price_per_unit": 25.0},\n'
            '    {"product": "elderberry", "units": 40, "price_per_unit": 22.0},\n'
            ']\n'
            'revenue_list = []\n'
            'for record in sales:\n'
            '    if record["units"] > 10:\n'
            '        revenue_list.append(record["units"] * record["price_per_unit"])\n'
            'total_revenue = sum(revenue_list)\n',
 'lists2': 'numbers = [10, 20, 30, 40, 50]\nfirst = numbers[0]\nnumbers[2] = 99\n',
 'lists3': 'items = ["apple", "banana"]\nitems.append("cherry")\nitems.insert(1, "mango")\n',
 'lists4': 'items = ["apple", "banana", "cherry", "date"]\n'
           'items.remove("banana")\n'
           'last = items.pop()\n',
 'lists5': 'letters = ["a", "b", "c", "d", "e", "f"]\n'
           'first_three = letters[:3]\n'
           'last_two = letters[-2:]\n'
           'middle = letters[2:5]\n',
 'lists6': 'scores = [42, 7, 99, 55, 3, 76]\nscores.sort()\ndesc = sorted(scores, reverse=True)\n',
 'lists7': 'fruits = ["apple", "banana", "cherry", "banana", "apple", "apple"]\n'
           'total = len(fruits)\n'
           'has_kiwi = "kiwi" in fruits\n'
           'apple_count = fruits.count("apple")\n',
 'lists8': 'temperatures = [0, 100, -40, 37, 212, -273]\n'
           'fahrenheit = []\n'
           'for temp in temperatures:\n'
           '    fahrenheit.append(temp * 9 / 5 + 32)\n',
 'lists9': 'matrix = [[1,2,3],[4,5,6],[7,8,9]]\n'
           'center = matrix[1][1]\n'
           'bottom_right = matrix[2][2]\n'
           'matrix[0][2] = 99\n',
 'loops1': 'total = 0\nfor n in range(1, 6):\n    total += n\n',
 'loops10': 'transactions = [\n'
            '    {"amount": 100, "type": "credit"},\n'
            '    {"amount": 0, "type": "debit"},\n'
            '    {"amount": 40, "type": "debit"},\n'
            '    {"amount": 200, "type": "credit"},\n'
            '    {"amount": 60, "type": "debit"},\n'
            ']\n'
            'summary = []\n'
            'balance = 0\n'
            'for index, tx in enumerate(transactions, start=1):\n'
            '    amount = tx["amount"]\n'
            '    if amount == 0:\n'
            '        continue\n'
            '    if tx["type"] == "credit":\n'
            '        balance += amount\n'
            '    else:\n'
            '        balance -= amount\n'
            '    summary.append({"index": index, "amount": amount, "balance": balance})\n',
 'loops2': 'fruits = ["apple", "banana", "cherry"]\n'
           'upper_fruits = []\n'
           'for fruit in fruits:\n'
           '    upper_fruits.append(fruit.upper())\n',
 'loops3': 'n = 5\ncountdown = []\nwhile n > 0:\n    countdown.append(n)\n    n -= 1\n',
 'loops4': 'numbers = [1,2,3,4,5,6,7,8,9,10]\n'
           'total = 0\n'
           'product = 1\n'
           'for n in numbers:\n'
           '    total += n\n'
           '    product *= n\n',
 'loops5': 'values = [3, 7, 2, 15, 8, 22]\n'
           'found = None\n'
           'i = 0\n'
           'while i < len(values):\n'
           '    if values[i] > 10:\n'
           '        found = values[i]\n'
           '        break\n'
           '    i += 1\n',
 'loops6': 'numbers = [1,2,3,4,5,6,7,8,9,10]\n'
           'evens = []\n'
           'for n in numbers:\n'
           '    if n % 2 != 0:\n'
           '        continue\n'
           '    evens.append(n)\n',
 'loops7': 'table = []\n'
           'for i in range(3):\n'
           '    row = []\n'
           '    for j in range(3):\n'
           '        row.append((i + 1) * (j + 1))\n'
           '    table.append(row)\n',
 'loops8': 'words = ["python", "is", "fun"]\n'
           'labeled = []\n'
           'for i, word in enumerate(words, start=1):\n'
           '    labeled.append(f"{i}: {word}")\n',
 'loops9': 'scores = {"Alice": 88, "Bob": 95, "Carol": 72, "Dave": 95 - 1}\n'
           'top_name = None\n'
           'top_score = -1\n'
           'for name, score in scores.items():\n'
           '    if score > top_score:\n'
           '        top_name = name\n'
           '        top_score = score\n',
 'modules1': 'import math\nresult = math.sqrt(144)\n',
 'modules2': 'from math import sqrt\nroot = sqrt(81)\n',
 'modules3': 'import math as m\ncircle_area = m.pi * 5 ** 2\nfloored = m.floor(7.9)\n',
 'modules4': 'import random\nrandom.seed(42)\npick = random.randint(1, 10)\n',
 'modules5': 'import string\ndigits = string.digits\nletters = string.ascii_letters\n',
 'modules6': 'module_name = __name__\n',
 'modules7': 'ran_as_script = False\nif __name__ == "__main__":\n    ran_as_script = True\n',
 'modules8': 'import math\n'
             'import random\n'
             'import statistics\n'
             'random.seed(0)\n'
             'data = [random.randint(1, 100) for _ in range(10)]\n'
             'data_mean = statistics.mean(data)\n'
             'data_max_sqrt = math.sqrt(max(data))\n',
 'oop_advanced1': 'class Animal:\n'
                  '    def speak(self):\n'
                  '        return "sound"\n'
                  '\n'
                  'class Dog(Animal):\n'
                  '    pass\n',
 'oop_advanced10': 'from abc import ABC, abstractmethod\n'
                   '\n'
                   'class Shape(ABC):\n'
                   '    @abstractmethod\n'
                   '    def area(self):\n'
                   '        pass\n'
                   '\n'
                   'class Square(Shape):\n'
                   '    def __init__(self, side):\n'
                   '        self.side = side\n'
                   '\n'
                   '    def area(self):\n'
                   '        return self.side * self.side\n',
 'oop_advanced11': 'class DictMixin:\n'
                   '    def to_dict(self):\n'
                   '        return dict(self.__dict__)\n'
                   '\n'
                   'class Product(DictMixin):\n'
                   '    def __init__(self, name, price):\n'
                   '        self.name = name\n'
                   '        self.price = price\n',
 'oop_advanced12': 'class Vector:\n'
                   '    def __init__(self, x, y):\n'
                   '        self.x = x\n'
                   '        self.y = y\n'
                   '\n'
                   '    def __add__(self, other):\n'
                   '        return Vector(self.x + other.x, self.y + other.y)\n',
 'oop_advanced2': 'class Person:\n'
                  '    def __init__(self, name):\n'
                  '        self.name = name\n'
                  '\n'
                  'class Employee(Person):\n'
                  '    def __init__(self, name, role):\n'
                  '        super().__init__(name)\n'
                  '        self.role = role\n',
 'oop_advanced3': 'class Square:\n'
                  '    def __init__(self, side):\n'
                  '        self.side = side\n'
                  '\n'
                  '    def area(self):\n'
                  '        return self.side * self.side\n'
                  '\n'
                  'class Rectangle:\n'
                  '    def __init__(self, width, height):\n'
                  '        self.width = width\n'
                  '        self.height = height\n'
                  '\n'
                  '    def area(self):\n'
                  '        return self.width * self.height\n'
                  '\n'
                  'def total_area(shapes):\n'
                  '    return sum(shape.area() for shape in shapes)\n',
 'oop_advanced4': 'class User:\n'
                  '    def __init__(self, name):\n'
                  '        self._name = name\n'
                  '\n'
                  '    @property\n'
                  '    def name(self):\n'
                  '        return self._name\n',
 'oop_advanced5': 'class Playlist:\n'
                  '    def __init__(self, songs):\n'
                  '        self.songs = songs\n'
                  '\n'
                  '    def __len__(self):\n'
                  '        return len(self.songs)\n',
 'oop_advanced6': 'class Point:\n'
                  '    def __init__(self, x, y):\n'
                  '        self.x = x\n'
                  '        self.y = y\n'
                  '\n'
                  '    def __repr__(self):\n'
                  '        return f"Point(x={self.x}, y={self.y})"\n',
 'oop_advanced7': 'class Book:\n'
                  '    def __init__(self, title, isbn):\n'
                  '        self.title = title\n'
                  '        self.isbn = isbn\n'
                  '\n'
                  '    def __eq__(self, other):\n'
                  '        if not isinstance(other, Book):\n'
                  '            return NotImplemented\n'
                  '        return self.isbn == other.isbn\n',
 'oop_advanced8': 'class Coordinate:\n'
                  '    def __init__(self, x, y):\n'
                  '        self.x = x\n'
                  '        self.y = y\n'
                  '\n'
                  '    @classmethod\n'
                  '    def from_text(cls, text):\n'
                  '        x_text, y_text = text.split(",")\n'
                  '        return cls(int(x_text), int(y_text))\n',
 'oop_advanced9': 'class Grade:\n'
                  '    @staticmethod\n'
                  '    def is_valid(percent):\n'
                  '        return 0 <= percent <= 100\n',
 'pathlib1': 'from pathlib import Path\npath = Path("notes/today.txt")\nfilename = path.name\n',
 'pathlib2': 'from pathlib import Path\n'
             'project = Path("pylings")\n'
             'source = project / "src" / "main.py"\n',
 'pathlib3': 'from pathlib import Path\n'
             'path = Path("docs/guide.md")\n'
             'parent = path.parent\n'
             'stem = path.stem\n'
             'suffix = path.suffix\n',
 'pathlib4': 'from pathlib import Path\n'
             'files = [Path("app.py"), Path("README.md"), Path("tests.py")]\n'
             'python_files = [path for path in files if path.suffix == ".py"]\n',
 'pathlib5': 'from pathlib import Path\n'
             'original = Path("reports/draft.txt")\n'
             'final = original.with_name("final.txt")\n',
 'pathlib6': 'from pathlib import Path\n'
             'source = Path("data/raw.csv")\n'
             'processed = source.with_suffix(".json")\n'
             'parts = processed.parts\n',
 'recursion1': 'def countdown(n):\n'
               '    if n == 0:\n'
               '        return [0]\n'
               '    return [n] + countdown(n - 1)\n',
 'recursion2': 'def factorial(n):\n'
               '    if n == 0:\n'
               '        return 1\n'
               '    return n * factorial(n - 1)\n',
 'recursion3': 'def recursive_sum(lst):\n'
               '    if not lst:\n'
               '        return 0\n'
               '    return lst[0] + recursive_sum(lst[1:])\n',
 'recursion4': 'def count_items(lst):\n'
               '    if not lst:\n'
               '        return 0\n'
               '    return 1 + count_items(lst[1:])\n',
 'recursion5': 'def fibonacci(n):\n'
               '    if n == 0:\n'
               '        return 0\n'
               '    if n == 1:\n'
               '        return 1\n'
               '    return fibonacci(n - 1) + fibonacci(n - 2)\n',
 'recursion6': 'def reverse_string(s):\n'
               '    if len(s) <= 1:\n'
               '        return s\n'
               '    return reverse_string(s[1:]) + s[0]\n',
 'recursion7': 'def deep_sum(nested):\n'
               '    if not nested:\n'
               '        return 0\n'
               '    first = nested[0]\n'
               '    rest = nested[1:]\n'
               '    if isinstance(first, list):\n'
               '        return deep_sum(first) + deep_sum(rest)\n'
               '    return first + deep_sum(rest)\n',
 'recursion8': 'def tree_depth(tree):\n'
               '    if not tree["children"]:\n'
               '        return 1\n'
               '    return 1 + max(tree_depth(child) for child in tree["children"])\n'
               '\n'
               'def tree_search(tree, target):\n'
               '    if tree["value"] == target:\n'
               '        return True\n'
               '    return any(tree_search(child, target) for child in tree["children"])\n',
 'regex1': 'import re\n'
           'text = "hello world"\n'
           'pattern = r"hello"\n'
           'result = re.match(pattern, text)\n',
 'regex10': 'import re\n'
            'log_line = "[ERROR] db.engine: connection refused"\n'
            'pattern = r"\\[(?P<level>\\w+)\\] (?P<logger>[\\w.]+): (?P<message>.+)"\n'
            'match = re.search(pattern, log_line)\n'
            'level = match.group("level")\n'
            'logger = match.group("logger")\n'
            'message = match.group("message")\n',
 'regex2': 'import re\n'
           'text = "I love python programming"\n'
           'pattern = r"python"\n'
           'result = re.search(pattern, text)\n',
 'regex3': 'import re\n'
           'text = "order 12 has 3 items and 450 points"\n'
           'numbers = re.findall(r"\\d+", text)\n',
 'regex4': 'import re\n'
           'text = "Hello world 123 foo_bar baz!"\n'
           'words = re.findall(r"[a-z]+", text)\n',
 'regex5': 'import re\n'
           'text = "requires python 3.10 or 2.7, not 1.x or 42"\n'
           'versions = re.findall(r"\\d+\\.\\d+", text)\n',
 'regex6': 'import re\n'
           'code = "ABCDE123"\n'
           'pattern = r"[A-Z]{5}\\d{3}"\n'
           'is_valid = bool(re.fullmatch(pattern, code))\n',
 'regex7': 'import re\n'
           'phone = "(415) 555-2671"\n'
           'pattern = r"\\((\\d{3})\\) \\d{3}-\\d{4}"\n'
           'match = re.search(pattern, phone)\n'
           'area_code = match.group(1)\n',
 'regex8': 'import re\n'
           'text = "This email is full of spam and junk, total spam!"\n'
           'pattern = r"spam|junk"\n'
           'clean = re.sub(pattern, "***", text)\n',
 'regex9': 'import re\n'
           'date_str = "2024-07-15"\n'
           'pattern = r"(?P<year>\\d{4})-(?P<month>\\d{2})-(?P<day>\\d{2})"\n'
           'match = re.search(pattern, date_str)\n'
           'year = match.group("year")\n'
           'month = match.group("month")\n'
           'day = match.group("day")\n',
 'sets1': 'primes = {2, 3, 5, 7}\n',
 'sets10': 'day1 = ["alice", "bob", "carol", "dave"]\n'
           'day2 = ["bob", "carol", "eve", "frank"]\n'
           's1 = set(day1)\n'
           's2 = set(day2)\n'
           'attended_both = s1 & s2\n'
           'attended_any = s1 | s2\n'
           'only_day1 = s1 - s2\n'
           'only_day2 = s2 - s1\n',
 'sets2': 'colors = {"red", "blue", "orange"}\ncolors.add("purple")\ncolors.discard("orange")\n',
 'sets3': 'fruits = {"apple", "banana", "cherry"}\n'
          'has_apple = "apple" in fruits\n'
          'has_grape = "grape" in fruits\n',
 'sets4': 'a = {1, 2, 3, 4}\nb = {3, 4, 5, 6}\ncombined = a | b\n',
 'sets5': 'a = {1, 2, 3, 4}\nb = {3, 4, 5, 6}\nshared = a & b\n',
 'sets6': 'a = {1, 2, 3, 4}\nb = {3, 4, 5, 6}\nonly_in_a = a - b\n',
 'sets7': 'numbers = [1, 2, 3, 2, 4, 1, 5, 3, 2, 4]\n'
          'unique = set(numbers)\n'
          'unique_count = len(unique)\n',
 'sets8': 'small = {2, 4}\n'
          'big = {1, 2, 3, 4, 5}\n'
          'is_subset = small <= big\n'
          'is_superset = big >= small\n',
 'sets9': 'numbers = [1, 2, 3, 4, 5, 6, 7]\n'
          'even_squares = {n * n for n in numbers if n % 2 == 0}\n',
 'strings1': 'greeting = "hello"\n',
 'strings10': 'item = "widget"\n'
              'qty = 42\n'
              'price = 3.99\n'
              'report = f"Item: {item} | Qty: {qty} | Price: ${price:.2f}"\n',
 'strings2': 'first = "Ada"\nlast = "Lovelace"\nfull_name = first + " " + last\n',
 'strings3': 'word = "python"\nfirst_char = word[0]\nlast_char = word[-1]\n',
 'strings4': 'sentence = "the quick brown fox"\nword = sentence[4:9]\n',
 'strings5': 'text = "Hello, World!"\n'
             'length = len(text)\n'
             'upper = text.upper()\n'
             'lower = text.lower()\n',
 'strings6': 'raw = "  I love cats and cats  "\n'
             'clean = raw.strip()\n'
             'replaced = clean.replace("cat", "dog")\n',
 'strings7': 'csv_line = "apple,banana,cherry"\n'
             'items = csv_line.split(",")\n'
             'rejoined = ", ".join(items)\n',
 'strings8': 'name = "Grace"\nage = 30\nmessage = f"Hello, {name}! You are {age} years old."\n',
 'strings9': 'sentence = "the quick brown fox jumps"\n'
             'has_fox = "fox" in sentence\n'
             'fox_index = sentence.find("fox")\n',
 'testing1': 'def double(x):\n    return x * 2\n\nresult = double(2)\nassert result == 4\n',
 'testing10': 'def sum_list(numbers):\n'
              '    return sum(numbers)\n'
              '\n'
              'def test_sum_list():\n'
              '    assert sum_list([]) == 0\n'
              '    assert sum_list([0]) == 0\n'
              '    assert sum_list([-1, -2]) == -3\n'
              '    assert sum_list([1, -1]) == 0\n'
              '    assert sum_list([1, 2, 3]) == 6\n',
 'testing11': 'class Counter:\n'
              '    def __init__(self):\n'
              '        self.value = 0\n'
              '\n'
              '    def increment(self):\n'
              '        self.value += 1\n'
              '\n'
              '    def reset(self):\n'
              '        self.value = 0\n'
              '\n'
              'def test_counter():\n'
              '    counter = Counter()\n'
              '    assert counter.value == 0\n'
              '    counter.increment()\n'
              '    assert counter.value == 1\n'
              '    counter.increment()\n'
              '    assert counter.value == 2\n'
              '    counter.reset()\n'
              '    assert counter.value == 0\n',
 'testing12': 'def is_palindrome(s):\n'
              '    s = s.lower().replace(" ", "")\n'
              '    return s == s[::-1]\n'
              '\n'
              'def word_count(s):\n'
              '    if not s.strip():\n'
              '        return 0\n'
              '    return len(s.split())\n'
              '\n'
              'def to_title_case(s):\n'
              '    return s.title()\n'
              '\n'
              'def truncate(s, max_len):\n'
              '    return s if len(s) <= max_len else s[:max_len] + "..."\n'
              '\n'
              'def test_palindrome():\n'
              '    assert is_palindrome("racecar") is True\n'
              '    assert is_palindrome("hello") is False\n'
              '    assert is_palindrome("") is True\n'
              '\n'
              'def test_word_count():\n'
              '    assert word_count("one two three") == 3\n'
              '    assert word_count("hello") == 1\n'
              '    assert word_count("") == 0\n'
              '\n'
              'def test_title_case():\n'
              '    assert to_title_case("hello world") == "Hello World"\n'
              '    assert to_title_case("pylings") == "Pylings"\n'
              '\n'
              'def test_truncate():\n'
              '    assert truncate("short", 10) == "short"\n'
              '    assert truncate("abcdef", 3) == "abc..."\n'
              '    assert truncate("abc", 3) == "abc"\n',
 'testing2': 'def square(x):\n'
             '    return x * x\n'
             '\n'
             'assert square(5) == 25, "5 squared should be 25"\n',
 'testing3': 'def add(a, b):\n'
             '    return a + b\n'
             '\n'
             'def test_add():\n'
             '    assert add(2, 3) == 5\n'
             '    assert add(0, 0) == 0\n',
 'testing4': 'def is_even(n):\n'
             '    return n % 2 == 0\n'
             '\n'
             'def test_is_even():\n'
             '    assert is_even(0) is True\n'
             '    assert is_even(2) is True\n'
             '    assert is_even(7) is False\n'
             '    assert is_even(-4) is True\n',
 'testing5': 'def clamp(value, lo, hi):\n'
             '    return max(lo, min(value, hi))\n'
             '\n'
             'def test_clamp():\n'
             '    assert clamp(5, 0, 10) == 5\n'
             '    assert clamp(-3, 0, 10) == 0\n'
             '    assert clamp(15, 0, 10) == 10\n'
             '    assert clamp(0, 0, 10) == 0\n'
             '    assert clamp(10, 0, 10) == 10\n',
 'testing6': 'def parse_positive(s):\n'
             '    n = int(s)\n'
             '    if n < 0:\n'
             '        raise ValueError(f"{n} is not positive")\n'
             '    return n\n'
             '\n'
             'def test_parse_positive():\n'
             '    assert parse_positive("42") == 42\n'
             '    try:\n'
             '        parse_positive("-1")\n'
             '        assert False, "expected ValueError"\n'
             '    except ValueError:\n'
             '        pass\n',
 'testing7': 'def divide(a, b):\n'
             '    if b == 0:\n'
             '        raise ValueError("cannot divide by zero")\n'
             '    return a / b\n'
             '\n'
             'def test_divide_message():\n'
             '    assert divide(10, 2) == 5.0\n'
             '    try:\n'
             '        divide(5, 0)\n'
             '        assert False, "expected ValueError"\n'
             '    except ValueError as e:\n'
             '        assert "zero" in str(e)\n',
 'testing8': 'def fahrenheit_to_celsius(f):\n'
             '    return round((f - 32) * 5 / 9, 10)\n'
             '\n'
             'def test_fahrenheit_to_celsius():\n'
             '    cases = [(32, 0.0), (212, 100.0), (98.6, 37.0), (-40, -40.0)]\n'
             '    for f, expected in cases:\n'
             '        assert abs(fahrenheit_to_celsius(f) - expected) < 1e-6, (\n'
             '            f"fahrenheit_to_celsius({f}) expected {expected}"\n'
             '        )\n',
 'testing9': 'def make_user():\n'
             '    return {"name": "Alice", "age": 30}\n'
             '\n'
             'def greet(user):\n'
             '    return f"Hello, {user[\'name\']}!"\n'
             '\n'
             'def test_user_greeting():\n'
             '    user = make_user()\n'
             '    assert greet(user) == "Hello, Alice!"\n',
 'tuples1': 'point = (3, 4)\n',
 'tuples10': 'results = [("Alice", 85), ("Bob", 42), ("Carol", 55), ("Diana", 91), ("Eve", 82)]\n'
             'top_student = max(results, key=lambda item: item[1])[0]\n'
             'average = sum(score for _, score in results) / len(results)\n'
             'passed = [name for name, score in results if score >= 60]\n',
 'tuples2': 'rgb = (255, 128, 0)\nred = rgb[0]\nblue = rgb[-1]\n',
 'tuples3': 'coordinates = (10, 20, 30)\nx, y, z = coordinates\n',
 'tuples4': 'solo = (42,)\n',
 'tuples5': 'original = (10, 20, 30)\nupdated = (original[0], 99, original[2])\n',
 'tuples6': 'def min_max(numbers):\n'
            '    return (min(numbers), max(numbers))\n'
            '\n'
            'result = min_max([4, 1, 7, 2, 9, 3])\n',
 'tuples7': 'a = 7\nb = 99\na, b = b, a\n',
 'tuples8': 'scores = (45, 85, 92, 55, 60, 74)\n'
            'passing = []\n'
            'for score in scores:\n'
            '    if score >= 60:\n'
            '        passing.append(score)\n',
 'tuples9': 'grid = {(0, 0): "origin", (1, 0): "right", (0, 1): "up"}\nlabel = grid[(1, 0)]\n',
 'type_hints1': 'count: int = 0\n',
 'type_hints2': 'def greet(name: str, times: int) -> str:\n    return (name + " ") * times\n',
 'type_hints3': 'def total(scores: list[int], labels: dict[str, int]) -> int:\n'
                '    return sum(scores) + sum(labels.values())\n',
 'type_hints4': 'def find_index(items: list[str], target: str) -> int | None:\n'
                '    try:\n'
                '        return items.index(target)\n'
                '    except ValueError:\n'
                '        return None\n',
 'type_hints5': 'def bounding_box(points: list[tuple[float, float]]) -> tuple[float, float, float, '
                'float]:\n'
                '    xs = [p[0] for p in points]\n'
                '    ys = [p[1] for p in points]\n'
                '    return (min(xs), min(ys), max(xs), max(ys))\n',
 'type_hints6': 'Vector = list[float]\n'
                '\n'
                'def scale(v: Vector, factor: float) -> Vector:\n'
                '    return [x * factor for x in v]\n',
 'type_hints7': 'from typing import Callable\n'
                '\n'
                'def apply_twice(func: Callable[[int], int], value: int) -> int:\n'
                '    return func(func(value))\n',
 'type_hints8': 'def summarise(records: list[dict[str, int]], key: str, default: int | None) -> '
                'dict[str, int | None]:\n'
                '    return {\n'
                '        "count": len(records),\n'
                '        "total": sum(r.get(key, default or 0) for r in records),\n'
                '        "missing": default,\n'
                '    }\n',
 'variables1': 'a = 0\nb = 0.0\nc = ""\n',
 'variables10': 'width = 3\n'
                'height = 4\n'
                'area = width * height\n'
                'perimeter = 2 * (width + height)\n'
                'diagonal = (width**2 + height**2) ** 0.5\n',
 'variables2': 'a = 10\nb = 3\nc = "hello"\n',
 'variables3': 'count = 7\nratio = 0.5\nis_ready = True\n',
 'variables4': 'score = 0\nscore = 20\nscore = 42\n',
 'variables5': 'total = 10\ntotal += 5\ntotal -= 3\ntotal *= 4\n',
 'variables6': 'x, y = 1, 2\n',
 'variables7': 'a = 10\nb = 20\na, b = b, a\n',
 'variables8': 'kind = type(3.14)\nas_int = int(3.14)\nas_str = str(42)\n',
 'variables9': 'TAX_RATE = 0.2\nprice = 50\ntotal_price = price * (1 + TAX_RATE)\n'}


def _source(solution_file: str) -> tuple[str, str]:
    path = Path(solution_file)
    name = path.stem
    try:
        source = ANSWERS[name]
    except KeyError as exc:
        raise RuntimeError(f"no reference solution for {name}") from exc
    return str(path), source


def apply(solution_file: str, namespace: dict[str, object]) -> None:
    filename, source = _source(solution_file)
    lines = source.splitlines(keepends=True)
    linecache.cache[filename] = (len(source), None, lines, filename)
    namespace["__file__"] = filename
    exec(compile(source, filename, "exec", dont_inherit=True), namespace)


def load(solution_file: str) -> dict[str, object]:
    filename, source = _source(solution_file)
    lines = source.splitlines(keepends=True)
    linecache.cache[filename] = (len(source), None, lines, filename)
    namespace: dict[str, object] = {
        "__name__": "__main__",
        "__file__": filename,
        "__package__": None,
    }
    exec(compile(source, filename, "exec", dont_inherit=True), namespace)
    return namespace
