#!/usr/bin/env python3
"""Fetch small local reference snippets from the official Python docs.

The generated snippets are committed so learners can use pythonlings offline.
Run from the repository root:

    python scripts/fetch_python_docs.py
"""

from __future__ import annotations

import argparse
import html
import json
import textwrap
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag


BASE_URL = "https://docs.python.org/3/"
OUTPUT = Path("pythonlings/docs")
MAX_LINES = 26


@dataclass(frozen=True)
class Source:
    topic: str
    title: str
    url: str
    summary: str


SOURCES: tuple[Source, ...] = (
    Source("variables", "Variables", BASE_URL + "tutorial/introduction.html#using-python-as-a-calculator", "Assigning names with `=` lets you keep values for later expressions."),
    Source("strings", "Strings", BASE_URL + "library/stdtypes.html#text-sequence-type-str", "Strings are immutable text sequences with indexing, slicing, and many useful methods."),
    Source("conditionals", "Conditionals", BASE_URL + "tutorial/controlflow.html#if-statements", "`if`, `elif`, and `else` choose which block runs based on boolean conditions."),
    Source("loops", "Loops", BASE_URL + "tutorial/controlflow.html#for-statements", "`for` loops iterate over items; `while` loops continue while a condition is true."),
    Source("functions", "Functions", BASE_URL + "tutorial/controlflow.html#defining-functions", "`def` creates reusable behavior with parameters, return values, and optional defaults."),
    Source("lists", "Lists", BASE_URL + "tutorial/datastructures.html#more-on-lists", "Lists are mutable ordered collections with methods such as `append`, `pop`, and `sort`."),
    Source("tuples", "Tuples", BASE_URL + "tutorial/datastructures.html#tuples-and-sequences", "Tuples group ordered values and are commonly unpacked into multiple names."),
    Source("dictionaries", "Dictionaries", BASE_URL + "tutorial/datastructures.html#dictionaries", "Dictionaries map keys to values and are the standard way to represent lookup tables."),
    Source("sets", "Sets", BASE_URL + "tutorial/datastructures.html#sets", "Sets store unique values and support membership tests and set operations."),
    Source("comprehensions", "Comprehensions", BASE_URL + "tutorial/datastructures.html#list-comprehensions", "Comprehensions build new collections by combining an expression with one or more loops."),
    Source("exceptions", "Exceptions", BASE_URL + "tutorial/errors.html#handling-exceptions", "`try` and `except` handle errors without crashing the whole program."),
    Source("file_io", "File I/O", BASE_URL + "tutorial/inputoutput.html#reading-and-writing-files", "`open` and `with` are the usual tools for reading and writing files safely."),
    Source("classes", "Classes", BASE_URL + "tutorial/classes.html#a-first-look-at-classes", "Classes combine data and behavior into reusable types."),
    Source("functional", "Functional Tools", BASE_URL + "howto/functional.html", "Functional style uses functions, iterators, and transformations as building blocks."),
    Source("decorators", "Decorators", BASE_URL + "reference/compound_stmts.html#function-definitions", "Decorators wrap or transform functions and classes with `@decorator` syntax."),
    Source("generators", "Generators", BASE_URL + "tutorial/classes.html#generators", "Generators produce values lazily with `yield` instead of returning a whole collection."),
    Source("context_managers", "Context Managers", BASE_URL + "reference/compound_stmts.html#the-with-statement", "Context managers run setup and cleanup around a block using `with`."),
    Source("dataclasses", "Dataclasses", BASE_URL + "library/dataclasses.html", "Dataclasses generate common class methods for data-focused classes."),
    Source("type_hints", "Type Hints", BASE_URL + "library/typing.html", "Type hints annotate expected values and help tools reason about your code."),
    Source("regex", "Regular Expressions", BASE_URL + "library/re.html", "The `re` module searches, matches, and transforms text using regular expressions."),
    Source("testing", "Testing", BASE_URL + "library/unittest.html", "Tests encode expected behavior so code can be checked repeatedly."),
    Source("recursion", "Recursion", BASE_URL + "tutorial/controlflow.html#defining-functions", "Recursive functions solve a problem by calling themselves on smaller inputs."),
    Source("modules", "Modules", BASE_URL + "tutorial/modules.html#modules", "Modules organize Python code into importable files and packages."),
    Source("collections", "Collections", BASE_URL + "library/collections.html", "`collections` provides specialized containers beyond the built-in list, dict, set, and tuple."),
    Source("itertools", "Itertools", BASE_URL + "library/itertools.html", "`itertools` provides fast iterator building blocks for loops and data pipelines."),
    Source("json", "JSON", BASE_URL + "library/json.html", "`json` converts between Python values and JSON text."),
    Source("datetime", "Datetime", BASE_URL + "library/datetime.html", "`datetime` represents dates, times, durations, and time zones."),
    Source("enums", "Enums", BASE_URL + "library/enum.html", "Enums define named constant values that are easier to read than raw literals."),
    Source("pathlib", "Pathlib", BASE_URL + "library/pathlib.html", "`pathlib.Path` represents filesystem paths with object-oriented helpers."),
    Source("oop_advanced", "Advanced OOP", BASE_URL + "tutorial/classes.html", "Advanced class patterns build on attributes, methods, inheritance, and special methods."),
    Source("async", "Asyncio", BASE_URL + "library/asyncio.html", "`asyncio` runs concurrent I/O-bound work with coroutines and an event loop."),
)


class SectionParser(HTMLParser):
    def __init__(self, target_id: str | None) -> None:
        super().__init__(convert_charrefs=True)
        self.target_id = target_id
        self.capture = target_id is None
        self.found = target_id is None
        self.section_depth = 0
        self.skip_depth = 0
        self.in_pre = False
        self.in_code = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag in {"script", "style", "nav", "footer"}:
            self.skip_depth += 1
            return

        if tag == "section":
            if self.capture:
                self.section_depth += 1
            elif attr.get("id") == self.target_id:
                self.capture = True
                self.found = True
                self.section_depth = 1

        if not self._collecting():
            return

        if tag in {"h1", "h2", "h3"}:
            self.parts.append("\n\n")
        elif tag == "p":
            self.parts.append("\n\n")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag == "pre":
            self.in_pre = True
            self.parts.append("\n\n```python\n")
        elif tag == "code" and not self.in_pre:
            self.in_code = True
            self.parts.append("`")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "nav", "footer"} and self.skip_depth:
            self.skip_depth -= 1
            return

        if self._collecting():
            if tag in {"p", "li"}:
                self.parts.append("\n")
            elif tag == "pre":
                self.in_pre = False
                self.parts.append("\n```\n")
            elif tag == "code" and self.in_code:
                self.in_code = False
                self.parts.append("`")

        if tag == "section" and self.capture and self.section_depth:
            self.section_depth -= 1
            if self.section_depth == 0:
                self.capture = False

    def handle_data(self, data: str) -> None:
        if self._collecting():
            self.parts.append(data)

    def _collecting(self) -> bool:
        return self.capture and self.skip_depth == 0


def fetch(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "pythonlings-doc-fetcher/0.1"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


def extract(html_text: str, url: str) -> str:
    _, anchor = urldefrag(url)
    parser = SectionParser(anchor or None)
    parser.feed(html_text)
    text = html.unescape("".join(parser.parts))
    lines = normalize_lines(text)
    if not parser.found or not lines:
        raise RuntimeError(f"could not extract docs section from {url}")
    return "\n".join(lines[:MAX_LINES]).strip()


def normalize_lines(text: str) -> list[str]:
    lines: list[str] = []
    blank = False
    for raw in text.splitlines():
        line = " ".join(raw.strip().replace("¶", "").split())
        if not line:
            if lines and not blank:
                lines.append("")
            blank = True
            continue
        lines.append(line)
        blank = False
    while lines and not lines[-1]:
        lines.pop()
    return lines


def render_markdown(source: Source, extracted: str) -> str:
    return (
        f"# {source.title}\n\n"
        f"Source: {source.url}\n\n"
        "This local reference is generated from the official Python documentation "
        "and trimmed for pythonlings.\n\n"
        f"{source.summary}\n\n"
        "## Extracted reference\n\n"
        f"{extracted}\n"
    )


def write_outputs(sources: tuple[Source, ...], output: Path) -> None:
    topics_dir = output / "topics"
    topics_dir.mkdir(parents=True, exist_ok=True)
    index = {"generated_from": BASE_URL, "topics": {}}

    for source in sources:
        print(f"fetch {source.topic}: {source.url}")
        html_text = fetch(source.url)
        extracted = extract(html_text, source.url)
        filename = f"topics/{source.topic}.md"
        (output / filename).write_text(
            render_markdown(source, extracted), encoding="utf-8"
        )
        index["topics"][source.topic] = {
            "title": source.title,
            "source_url": source.url,
            "file": filename,
        }

    (output / "index.json").write_text(
        json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output / "NOTICE.md").write_text(
        textwrap.dedent(
            """\
            # Bundled Python Documentation Snippets

            These snippets are generated from the official Python documentation at
            https://docs.python.org/3/ and trimmed for use inside pythonlings.

            Python documentation pages are licensed under the Python Software
            Foundation License Version 2. Examples, recipes, and other code in the
            documentation are additionally licensed under the Zero Clause BSD License.
            See https://docs.python.org/3/copyright.html for details.
            """
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    write_outputs(SOURCES, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
