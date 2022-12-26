from util.prelude import *


@dataclass
class Unknown:
    ...


@dataclass
class Dependency:
    op: str
    left: str
    right: str

    def names(self) -> Iterable[str]:
        return [self.left, self.right]

    def __str__(self) -> str:
        return f"{self.left} {self.op} {self.right}"


@dataclass
class Monkey:
    name: str
    value: int | Dependency | Unknown
    depth: int | None = None


def parse_monkeys(input: str) -> dict[str, Monkey]:
    monkeys = {}
    for name, left, op, right, val in findall(
        r"(\w+): (?:(\w+) ([+\-/*]) (\w+)|(\d+))", input
    ):
        if val:
            monkey = Monkey(name, int(val))
        else:
            monkey = Monkey(name, Dependency(op, left, right))
        monkeys[name] = monkey
    return monkeys


def calc_depths(monkeys: dict[str, Monkey]) -> None:
    def calc_depth(monkey: Monkey):
        if monkey.depth is None:
            if type(monkey.value) == int:
                depth = 0
            else:
                names = monkey.value.names()
                depth = max(calc_depth(monkeys[name]) for name in names) + 1
            monkey.depth = depth
        return monkey.depth

    for m in monkeys.values():
        calc_depth(m)


def part1(input: str):
    monkeys = parse_monkeys(input)
    calc_depths(monkeys)

    eval_order = sorted(monkeys.values(), key=attrgetter("depth"))
    for monkey in eval_order:
        if type(monkey.value) == Dependency:
            names = monkey.value.names()
            values = {name: monkeys[name].value for name in names}
            monkey.value = int(eval(str(monkey.value), values))
    return monkeys["root"].value


def part2(input: str):
    monkeys = parse_monkeys(input)
    calc_depths(monkeys)
    eval_order = sorted(monkeys.values(), key=attrgetter("depth"))

    root = monkeys["root"]
    left = root.value.left
    right = root.value.right
    left_set = set([root.value.left])
    right_set = set([root.value.right])
    for monkey in reversed(eval_order[:-1]):
        if type(monkey.value) == int:
            continue
        names = monkey.value.names()
        if monkey.name in left_set:
            left_set.update(names)
        else:
            right_set.update(names)

    if "humn" not in right_set:
        left_set, right_set = right_set, left_set
        left, right = right, left

    for monkey in eval_order:
        if monkey.name not in left_set or type(monkey.value) != Dependency:
            continue
        names = monkey.value.names()
        values = {name: monkeys[name].value for name in names}
        monkey.value = int(eval(str(monkey.value), values))

    monkeys["humn"].value = Unknown()

    for monkey in eval_order:
        if monkey.name not in right_set or type(monkey.value) != Dependency:
            continue
        names = monkey.value.names()
        values = {name: monkeys[name].value for name in names}
        if any(type(value) != int for value in values.values()):
            continue
        monkey.value = int(eval(str(monkey.value), values))

    yell = monkeys[left].value

    for monkey in reversed(eval_order):
        if monkey.name not in right_set or type(monkey.value) != Dependency:
            continue
        ml = monkeys[monkey.value.left]
        mr = monkeys[monkey.value.right]
        if type(ml.value) == int:
            assert type(mr.value) != int
            match monkey.value.op:
                case "+":
                    yell -= ml.value
                case "-":
                    yell = ml.value - yell
                case "*":
                    yell //= ml.value
                case "/":
                    yell = ml.value / yell
        elif type(mr.value) == int:
            assert type(ml.value) != int
            match monkey.value.op:
                case "+":
                    yell -= mr.value
                case "-":
                    yell += mr.value
                case "*":
                    yell //= mr.value
                case "/":
                    yell *= mr.value

    return yell


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
    assert part2(example) == 301
