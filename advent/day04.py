from util.prelude import *


def overlaps_completely(a1, a2, b1, b2):
    return a1 <= b1 and a2 >= b2 or b1 <= a1 and b2 >= a2


def overlaps_partially(a1, a2, b1, b2):
    return (
        (a1 <= b1 and a2 >= b1)
        or (a1 <= b2 and a1 >= b2)
        or (b1 <= a1 and b2 >= a1)
        or (b1 <= a2 and b2 >= a2)
    )


def count_overlaps(assignments, overlaps):
    total = 0
    for matches in findall(r"(\d+)-(\d+),(\d+)-(\d+)", assignments):
        a1, a2, b1, b2 = map(int, matches)
        if overlaps(a1, a2, b1, b2):
            total += 1
    return total


def part1(input):
    return count_overlaps(input, overlaps_completely)


def part2(input):
    return count_overlaps(input, overlaps_partially)


example = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""


def test_part1():
    assert part1(example) == 2


def test_part2():
    assert part2(example) == 4
