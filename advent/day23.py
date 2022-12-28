from util.prelude import *


def parse_input(input):
    lines = input.strip().split("\n")
    return {
        (x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "#"
    }


adjacent = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))

quadrants = [
    ((0, 1, 2), (0, -1)),
    ((5, 6, 7), (0, 1)),
    ((0, 3, 5), (-1, 0)),
    ((2, 4, 7), (1, 0)),
]


def tick(elves: set[Vec2D], d0: int):
    candidates = []
    for elf in elves:
        x, y = elf
        if any((x + dx, y + dy) in elves for dx, dy in adjacent):
            candidates.append(elf)

    proposals = defaultdict(list)
    for elf in candidates:
        x, y = elf
        for i in range(4):
            indexes, move = quadrants[(d0 + i) % 4]
            if all(
                (x + dx, y + dy) not in elves
                for dx, dy in (adjacent[i] for i in indexes)
            ):
                dx, dy = move
                proposals[(x + dx, y + dy)].append(elf)
                break

    for final, proposers in proposals.items():
        if len(proposers) > 1:
            continue
        elf = proposers[0]
        elves.remove(elf)
        elves.add(final)


def get_bounds(elves: set[Vec2D]) -> tuple[int, int, int, int]:
    x0, _ = min(elves, key=get_x)
    x1, _ = max(elves, key=get_x)
    _, y0 = min(elves, key=get_y)
    _, y1 = max(elves, key=get_y)
    return x0, x1 + 1, y0, y1 + 1


def count_empty(elves: set[Vec2D]) -> int:
    x0, x1, y0, y1 = get_bounds(elves)
    return (x1 - x0) * (y1 - y0) - len(elves)


def debug(elves: set[Vec2D]):
    x0, x1, y0, y1 = get_bounds(elves)
    for y in range(y0, y1):
        out = ""
        for x in range(x0, x1):
            out += "#" if (x, y) in elves else "."
        print(out)
    print("")


def part1(input: str):
    elves = parse_input(input)
    d0 = 0
    for _ in range(10):
        tick(elves, d0)
        d0 = (d0 + 1) % 4
    return count_empty(elves)


def part2(input: str):
    raise NotImplementedError()


example = """..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............
"""


def test_part1():
    assert part1(example) == 110


def test_part2():
    assert part2(example) == 0
