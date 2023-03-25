# Pylings

Rustlings is an interactive program designed to teach Rust programming language by example. It offers a series of exercises containing code with errors, such as syntax issues or failed tests, which the user must fix before proceeding to the next exercise. This program has been highly popular and effective in teaching Rust to new learners.

In an effort to emulate this successful approach, PyLings aims to be a similar program for Python. With a similar interactive learning experience, PyLings offers a range of exercises that teach Python through example, with broken code that the user must fix before moving on to the next task.


## Table of Contents

- [Pylings](#pylings)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
  - [Running the Exercises](#running-the-exercises)
  - [Project Structure](#project-structure)
    - [Contributing](#contributing)

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

### Contributing
We welcome contributions to PyLings! If you find any issues or have ideas for new exercises, feel free to open a new issue or submit a pull request.

To contribute, follow these steps:

Fork the repository
Create a new branch for your changes
Make your changes and commit them with descriptive messages
Push your changes to your fork
Open a pull request
We'll review your changes and merge them if they meet our criteria.

Thank you for contributing to PyLings!