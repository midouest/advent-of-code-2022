from util.prelude import *


def size(map):
    return len(map[0]), len(map)


def coords(map, values):
    w, h = size(map)
    return ((x, y) for y in range(h) for x in range(w) if map[y][x] in values)


def find(map, values):
    return next(coords(map, values))


class HeightMapSearch(Search):
    def __init__(self, map, start):
        self.map = map
        self.w, self.h = size(self.map)
        self.start = start
        self.end = find(map, "E")

    def initial(self):
        return self.start

    def lookup(self, node):
        x, y = node
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return None
        return self.map[y][x]

    def height(self, node):
        value = self.lookup(node)
        if value == "S":
            return "a"
        if value == "E":
            return "z"
        return value

    def goal(self, node):
        return self.lookup(node) == "E"

    def traversable(self, current, neighbor):
        h = self.height(current)
        nh = self.height(neighbor)
        return nh is not None and ord(nh) - ord(h) <= 1

    def neighbors(self, node):
        x, y = node
        return filter(
            lambda neighbor: self.traversable(node, neighbor),
            [(x + dx, y + dy) for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]],
        )


def parse_input(input: str):
    return input.strip().split()


def path_length(map, start):
    search = HeightMapSearch(map, start)
    path = search.bfs()
    if not path:
        return inf
    return len(path) - 1


def part1(input: str):
    map = parse_input(input)
    return path_length(map, coords(map, "S"))


def part2(input: str):
    map = parse_input(input)
    return path_length(map, coords(map, "Sa"))


example = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""


def test_part1():
    assert part1(example) == 31


def test_part2():
    assert part2(example) == 29
