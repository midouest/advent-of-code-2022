import re
from collections import deque


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


def flood(coord, drops, pockets, air):
    frontier = deque([(coord)])
    visited = set(frontier)
    while frontier:
        x, y, z = frontier.popleft()
        if x == 0 or y == 0 or z == 0 or x == 19 or y == 19 or z == 19:
            return visited, False
        for dx, dy, dz in deltas:
            neighbor = (x + dx, y + dy, z + dz)
            if neighbor in air:
                return visited, False
            if neighbor in pockets:
                return visited, True
            if neighbor in visited or neighbor in drops:
                continue
            frontier.append(neighbor)
            visited.add(neighbor)
    return visited, True


def part2(input: str):
    drops = set()
    for matches in re.findall(r"(\d+),(\d+),(\d+)", input):
        drops.add(tuple(map(int, matches)))

    pockets = set()
    air = set()
    for x, y, z in drops:
        for dx, dy, dz in deltas:
            neighbor = (x + dx, y + dy, z + dz)
            if neighbor in drops or neighbor in pockets or neighbor in air:
                continue
            visited, trapped = flood(neighbor, drops, pockets, air)
            if trapped:
                pockets |= visited
            else:
                air |= visited

    total = 0
    for x, y, z in air:
        for dx, dy, dz in deltas:
            neighbor = (x + dx, y + dy, z + dz)
            if neighbor in drops:
                total += 1

    return total


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
