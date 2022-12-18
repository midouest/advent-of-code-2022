# advent-of-code-2022

Solutions to Advent of Code 2022 in Python

## Requirements

- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [Pipenv](https://pipenv.pypa.io/en/latest/)

## Installation

Pipenv is used to manage dependencies:

```bash
pipenv install --dev  # install all dependencies
pipenv shell          # activate the virtualenv in your shell
```

## Tests

[pytest](https://docs.pytest.org/en/7.2.x/) is used to test solutions on example inputs:

```bash
python -m pytest  # run the full test suite
```

## Command-line interface

Place your advent of code session cookie in the `.session` file in the root of the repository.

### Generate

Download the input for a given day and generate a solution template using the `g` command:

```bash
./a g 1     # download input and create stub solution
./a g 1 -i  # download input only
```

### Run

Solve one or more days/parts using the `r` command:

```bash
./a r         # run all days and parts
./a r 1       # run day 1, all parts
./a r 1 1     # run day 1, part 1
./a r 1 1 -s  # run day 1, part 1 and submit the answer
```
