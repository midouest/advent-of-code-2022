from util.prelude import *


def sign(n):
    return 1 if n > 0 else -1 if n < 0 else 0


def move(rope, axis, amt, step):
    off_axis = 1 - axis
    coords = set()
    for _ in range(amt):
        head = rope[0]
        head[axis] += step
        for knot in rope[1:]:
            d_axis = head[axis] - knot[axis]
            d_off_axis = head[off_axis] - knot[off_axis]
            if abs(d_axis) >= 2 or abs(d_off_axis) >= 2:
                knot[axis] += sign(d_axis)
                knot[off_axis] += sign(d_off_axis)
            head = knot
        coords.add(tuple(knot))
    return coords


dirs = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (1, 1),
    "D": (1, -1),
}


def simulate(input, length):
    rope = [[0, 0] for _ in range(length)]
    visited = set([(0, 0)])
    for dir, amt in findall(r"(R|L|U|D) (\d+)", input):
        amt = int(amt)
        axis, step = dirs[dir]
        coords = move(rope, axis, amt, step)
        visited.update(coords)
    return len(visited)


def part1(input: str):
    return simulate(input, 2)


def part2(input: str):
    return simulate(input, 10)


small_example = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

large_example = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""


def test_part1():
    assert part1(small_example) == 13


def test_part2():
    assert part2(small_example) == 1
    assert part2(large_example) == 36
