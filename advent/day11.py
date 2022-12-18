from util.prelude import *


@dataclass
class Monkey:
    items: deque[int]
    op: Callable[[int, int], int]
    test: int
    true: int
    false: int


def parse_op(line):
    operator, operand = line[23:].split(" ")
    op = add if operator == "+" else mul
    if operand == "old":
        return lambda old: op(old, old)
    return lambda old: op(old, int(operand))


def clean_input(input: str) -> list[Monkey]:
    monkeys = []
    for block in input.split("\n\n"):
        lines = block.split("\n")
        monkeys.append(
            Monkey(
                items=deque([int(s) for s in lines[1][18:].split(", ")]),
                op=parse_op(lines[2]),
                test=int(lines[3][21:]),
                true=int(lines[4][29:]),
                false=int(lines[5][30:]),
            )
        )
    return monkeys


def simulate(input, rounds, divisor):
    monkeys = clean_input(input)
    gcd = prod(monkey.test for monkey in monkeys)
    activity = defaultdict(int)
    for _ in range(rounds):
        for i, monkey in enumerate(monkeys):
            while monkey.items:
                old = monkey.items.popleft()
                new = (monkey.op(old) // divisor) % gcd
                throw_to = monkey.true if new % monkey.test == 0 else monkey.false
                monkeys[throw_to].items.append(new)
                activity[i] += 1
    inspections = sorted(activity.values(), reverse=True)
    return prod(inspections[:2])


def part1(input: str):
    return simulate(input, 20, 3)


def part2(input: str):
    return simulate(input, 10000, 1)


example = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


def test_part1():
    assert part1(example) == 10605


def test_part2():
    assert part2(example) == 2713310158
