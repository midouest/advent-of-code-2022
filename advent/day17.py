from itertools import cycle


def rocks_iter():
    return cycle(range(5))


def jets_iter(input: str):
    return cycle(input.strip())


left = {
    0: [(-1, 0)],
    1: [(0, 0), (-1, 1), (0, 2)],
    2: [(-1, 0), (1, 1), (1, 2)],
    3: [(-1, 0), (-1, 1), (-1, 2), (-1, 3)],
    4: [(-1, 0), (-1, 1)],
}


def move_left(rock, x, y, chamber):
    if x == 0:
        return x, y

    deltas = left[rock]
    if any(chamber.get((x + dx, y + dy)) for dx, dy in deltas):
        return x, y

    return x - 1, y


right = {
    0: [(4, 0)],
    1: [(2, 0), (3, 1), (2, 2)],
    2: [(3, 0), (3, 1), (3, 2)],
    3: [(1, 0), (1, 1), (1, 2), (1, 3)],
    4: [(2, 0), (2, 1)],
}

widths = {
    0: 4,
    1: 3,
    2: 3,
    3: 1,
    4: 2,
}


def move_right(rock, x, y, chamber):
    if x + widths[rock] > 6:
        return x, y

    deltas = right[rock]
    if any(chamber.get((x + dx, y + dy)) for dx, dy in deltas):
        return x, y

    return x + 1, y


moves = {"<": move_left, ">": move_right}


down = {
    0: [(0, -1), (1, -1), (2, -1), (3, -1)],
    1: [(0, 0), (1, -1), (2, 0)],
    2: [(0, -1), (1, -1), (2, -1)],
    3: [(0, -1)],
    4: [(0, -1), (1, -1)],
}

blocks = {
    0: [(0, 0), (1, 0), (2, 0), (3, 0)],
    1: [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    2: [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    3: [(0, 0), (0, 1), (0, 2), (0, 3)],
    4: [(0, 0), (1, 0), (0, 1), (1, 1)],
}

heights = {
    0: 1,
    1: 3,
    2: 3,
    3: 4,
    4: 2,
}


def move_down(rock, x, y, chamber):
    if y == 0:
        return x, y, False

    deltas = down[rock]
    if any(chamber.get((x + dx, y + dy)) for dx, dy in deltas):
        return x, y, False

    return x, y - 1, True


def debug(chamber, height):
    for y in range(height, -1, -1):
        row = "".join(chamber.get((x, y), ".") for x in range(7))
        print(row)


def simulate(input: str, n: int):
    jets = jets_iter(input)
    rocks = rocks_iter()
    height = 0
    chamber = {}
    for i in range(n):
        x, y = 2, height + 3
        rock = next(rocks)
        falling = True
        while falling:
            jet = next(jets)
            move = moves[jet]
            x, y = move(rock, x, y, chamber)
            x, y, falling = move_down(rock, x, y, chamber)

        for dx, dy in blocks[rock]:
            chamber[(x + dx, y + dy)] = "#"
        height = max(height, y + heights[rock])
    return height


def part1(input: str):
    return simulate(input, 2022)


def part2(input: str):
    return simulate(input, 1000000000000)


example = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""


def test_part1():
    assert part1(example) == 3068


def test_part2():
    assert part2(example) == 1514285714288
