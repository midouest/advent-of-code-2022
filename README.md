# advent-of-code-2022

Solutions to Advent of Code 2022 in Python

## Command-line interface

Place your advent of code session cookie in the `.session` file in the root of the repository.

### Generate

Download the input for a given day and generate a solution template using the `g` command:

```bash
./a g 1     # Download input and create stub solution
./a g 1 -i  # Download input only
```

### Run

Solve one or more days/parts using the `r` command:

```bash
./a r         # run all days and parts
./a r 1       # run day 1, all parts
./a r 1 1     # run day 1, part 1
./a r 1 1 -s  # run day 1, part 1 and submit the answer
```
