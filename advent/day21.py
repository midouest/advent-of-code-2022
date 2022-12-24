from util.prelude import *


@dataclass
class Dependency:
    op: str
    names: list[str]


@dataclass
class Monkey:
    name: str
    value: int | Dependency
    depth: int | None = None


pattern = r"(\w+): (?:((\w+) [+\-/*] (\w+))|(\d+))"


def parse_monkeys(input: str) -> dict[str, Monkey]:
    monkeys = {}
    for name, op, left, right, val in findall(pattern, input):
        if val:
            monkey = Monkey(name, int(val))
        else:
            monkey = Monkey(name, Dependency(op, [left, right]))
        monkeys[name] = monkey
    return monkeys


def calc_depths(monkeys: dict[str, Monkey]) -> None:
    def calc_depth(monkey: Monkey):
        if monkey.depth is None:
            if type(monkey.value) == int:
                depth = 0
            else:
                depth = (
                    max(calc_depth(monkeys[name]) for name in monkey.value.names) + 1
                )
            monkey.depth = depth
        return monkey.depth

    for m in monkeys.values():
        calc_depth(m)


def find_root(input: str):
    monkeys = parse_monkeys(input)
    calc_depths(monkeys)
    eval_order = sorted(monkeys.values(), key=attrgetter("depth"))
    for monkey in eval_order:
        if type(monkey.value) == Dependency:
            values = {name: monkeys[name].value for name in monkey.value.names}
            monkey.value = int(eval(monkey.value.op, values))
    return monkeys["root"].value


def part1(input: str):
    return find_root(input)


def part2(input: str):
    raise NotImplementedError()


example = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""


def test_part1():
    assert part1(example) == 152


def test_part2():
    assert part2(example) == 0
