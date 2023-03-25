# Pylings

Pylings is a collection of coding exercises designed to help Python programmers improve their skills by providing a series of code snippets with intentional errors. The goal of Pylings is to challenge your understanding of Python syntax, common pitfalls, and best practices.

## Table of Contents

- [Pylings](#pylings)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
  - [Running the Exercises](#running-the-exercises)
  - [Project Structure](#project-structure)

## Getting Started

### Prerequisites

Before you start working with Pylings, you'll need to have the following software installed on your computer:

- Python 3.6 or later
- pytest

To install pytest, run the following command:

```bash
pip install pytest

```

## Running the Exercises
To run the tests for all exercises, simply execute the pylings.sh script:
    
```bash
    ./pylings.sh
```
## Project Structure

The project is organized as follows:
├── exercises
│   ├── __init__.py
│   ├── functions
│   │   └── fuctions1.py
│   └── variables
│       ├── __init__.py
│       ├── variables1.py
│       └── variables2.py
├── pylings.py
├── pylings.sh
└── tests
    ├── functions
    │   └── fuctions1_test.py
    └── variables
        ├── variables1_test.py
        └── variables2_test.py



The exercises directory contains the code snippets with intentional errors. Each exercise is in its own file, organized into subdirectories by topic (e.g. functions, variables).

The tests directory contains the test files for each exercise. Each test file should have the same name as the corresponding exercise file, with _test appended to the end (e.g. variables1.py -> variables1_test.py). The test files should be organized into subdirectories that mirror the structure of the exercises