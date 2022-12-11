# advent-of-code-2022

Solutions to Advent of Code 2022 in Python

## Command-line interface

Place your advent of code session cookie in the `.session` file in the root of the repository.

### Generate

Download the input for a given day and generate a solution template using the `gen` command:

```bash
./cli gen 1          # Download input and create stub solution
./cli gen 1 --input  # Download input only
```

### Run

Solve one or more days/parts using the `run` command:

```bash
./cli run               # run all days and parts
./cli run 1             # run day 1, all parts
./cli run 1 1           # run day 1, part 1
./cli run 1 1 --submit  # run day 1, part 1 and submit the answer
```
