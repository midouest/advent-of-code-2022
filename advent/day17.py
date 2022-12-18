from util.prelude import *

left = {
    0: [(-1, 0)],
    1: [(0, 0), (-1, 1), (0, 2)],
    2: [(-1, 0), (1, 1), (1, 2)],
    3: [(-1, 0), (-1, 1), (-1, 2), (-1, 3)],
    4: [(-1, 0), (-1, 1)],
}


def move_left(rock, x, y, chamber):
    deltas = left[rock]
    if any((x + dx, y + dy) in chamber or x + dx < 0 for dx, dy in deltas):
        return x, y

    return x - 1, y


right = {
    0: [(4, 0)],
    1: [(2, 0), (3, 1), (2, 2)],
    2: [(3, 0), (3, 1), (3, 2)],
    3: [(1, 0), (1, 1), (1, 2), (1, 3)],
    4: [(2, 0), (2, 1)],
}


def move_right(rock, x, y, chamber):
    deltas = right[rock]
    if any((x + dx, y + dy) in chamber or x + dx > 6 for dx, dy in deltas):
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


def move_down(rock, x, y, chamber):
    deltas = down[rock]
    if any((x + dx, y + dy) in chamber or y + dy < 0 for dx, dy in deltas):
        return x, y, False

    return x, y - 1, True


def simulate(input: str, n: int):
    input = input.strip()
    height = 0
    chamber = set()
    j = 0
    memo = defaultdict(int)
    cycle = []
    cycled = False
    heights = []
    for i in range(n):
        rock = i % 5
        jet_index = j % len(input)
        initial_state = (rock, jet_index)
        if initial_state in memo:
            if (
                len(cycle) > 0
                and cycle[0][1] == initial_state
                and memo[initial_state] == 2
            ):
                cycled = True
                break
            cycle.append((i, initial_state))
        else:
            cycle = []
        memo[initial_state] += 1

        x, y = 2, height + 3
        falling = True
        while falling:
            jet_index = j % len(input)
            jet = input[jet_index]
            move = moves[jet]
            x, y = move(rock, x, y, chamber)
            x, y, falling = move_down(rock, x, y, chamber)
            j += 1

        for dx, dy in blocks[rock]:
            chamber.add((x + dx, y + dy))
        height = max(height, y + dy + 1)
        heights.append(height)

    if not cycled:
        return height

    cycle_start, _ = cycle[0]
    pre_cycle = cycle_start - 1
    cycle_length = len(cycle)

    h0 = heights[pre_cycle]
    h1 = heights[pre_cycle + cycle_length]
    cycle_height = h1 - h0

    remaining = n - i
    complete_remaining = remaining // cycle_length
    height += complete_remaining * cycle_height

    partial_remaining = remaining % cycle_length
    if partial_remaining > 0:
        h2 = heights[pre_cycle + partial_remaining]
        height += h2 - h0

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
