from util.prelude import *


def between(a, b):
    a, b = min(a, b), max(a, b)
    return range(a, b + 1)


def parse_input(input):
    cave = {}
    for line in input.strip().split("\n"):
        matches = findall("(\d+),(\d+)", line)
        match = matches[0]
        x1, y1 = map(int, match)
        for match in matches[1:]:
            x2, y2 = map(int, match)
            for y in between(y1, y2):
                for x in between(x1, x2):
                    cave[(x, y)] = "#"
            x1, y1 = x2, y2
    return cave


def part1(input: str):
    cave = parse_input(input)
    _, abyss = max(cave.keys(), key=itemgetter(1))
    while True:
        x, y = 500, 0
        while True:
            candidates = ((x + dx, y + dy) for dx, dy in [(0, 1), (-1, 1), (1, 1)])
            coord = next((coord for coord in candidates if not cave.get(coord)), None)
            if not coord:
                break
            x, y = coord
            if y == abyss:
                return Counter(cave.values())["o"]
        cave[(x, y)] = "o"


def part2(input: str):
    cave = parse_input(input)
    floor = max(map(itemgetter(1), cave.keys())) + 2
    while True:
        x, y = 500, 0
        while True:
            candidates = ((x + dx, y + dy) for dx, dy in [(0, 1), (-1, 1), (1, 1)])
            coord = next(
                ((x, y) for x, y in candidates if y < floor and not cave.get((x, y))),
                None,
            )
            if not coord:
                break
            x, y = coord
        cave[(x, y)] = "o"
        if x == 500 and y == 0:
            return Counter(cave.values())["o"]


example = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""


def test_part1():
    assert part1(example) == 24


def test_part2():
    assert part2(example) == 93
