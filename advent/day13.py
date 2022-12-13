from functools import cmp_to_key
from math import prod
from util.iterator import chunks


def parse_input(input):
    return [eval(line) for pair in input.strip().split("\n\n") for line in pair.split()]


def compare(left, right):
    if type(left) == int and type(right) == int:
        return left - right
    elif type(left) == list and type(right) == list:
        results = (compare(l, r) for l, r in zip(left, right))
        result = next((result for result in results if result != 0), None)
        if result is not None:
            return result
        return len(left) - len(right)
    elif type(left) == int and type(right) == list:
        return compare([left], right)
    else:
        return compare(left, [right])


def part1(input: str):
    return sum(
        i + 1
        for i, (left, right) in enumerate(chunks(parse_input(input), 2))
        if compare(left, right) < 0
    )


def part2(input: str):
    dividers = [[[2]], [[6]]]
    packets = parse_input(input) + dividers
    packets.sort(key=cmp_to_key(compare))
    return prod(packets.index(divider) + 1 for divider in dividers)


example = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""


def test_part1():
    assert part1(example) == 13


def test_part2():
    assert part2(example) == 140
