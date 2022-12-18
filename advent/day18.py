import re
from operator import add


deltas = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]


def part1(input: str):
    drops = set()
    total = 0
    for matches in re.findall(r"(\d+),(\d+),(\d+)", input):
        x, y, z = map(int, matches)
        total += 6
        drops.add((x, y, z))
        for dx, dy, dz in deltas:
            if (x + dx, y + dy, z + dz) in drops:
                total -= 2
    return total


def part2(input: str):
    raise NotImplementedError()


example = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""


def test_part1():
    assert part1(example) == 64


def test_part2():
    assert part2(example) == 58
