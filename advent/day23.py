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

    moved = 0
    for final, movers in proposals.items():
        if len(movers) > 1:
            continue
        elf = movers[0]
        elves.remove(elf)
        elves.add(final)
        moved += 1

    return (d0 + 1) % 4, moved


def get_bounds(elves: set[Vec2D]) -> tuple[int, int, int, int]:
    x0, _ = min(elves, key=get_x)
    x1, _ = max(elves, key=get_x)
    _, y0 = min(elves, key=get_y)
    _, y1 = max(elves, key=get_y)
    return x0, x1 + 1, y0, y1 + 1


def count_empty(elves: set[Vec2D]) -> int:
    x0, x1, y0, y1 = get_bounds(elves)
    return (x1 - x0) * (y1 - y0) - len(elves)


def part1(input: str):
    elves = parse_input(input)
    d0 = 0
    for _ in range(10):
        d0, _ = tick(elves, d0)
    return count_empty(elves)


def part2(input: str):
    elves = parse_input(input)
    d0 = 0
    for i in count(1):
        d0, moved = tick(elves, d0)
        if not moved:
            break
    return i


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
    assert part2(example) == 20
