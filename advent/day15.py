from util.prelude import *

pattern = r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"


def parse_input(input):
    return [
        (sx, sy, bx, by, manhattan((sx, sy), (bx, by)))
        for sx, sy, bx, by in (
            tuple(map(int, matches)) for matches in findall(pattern, input)
        )
    ]


def find_coverage(readings, y):
    coverage, beacons = set(), set()
    for sx, sy, bx, by, r in readings:
        dx = r - abs(y - sy)
        if dx < 0:
            continue
        x1, x2 = sx - dx, sx + dx
        coverage.add((x1, x2))
        if by == y:
            beacons.add(bx)

    coverage = sorted(coverage, key=itemgetter(0))

    merged = []
    a1, a2 = coverage[0]
    for b1, b2 in coverage[1:]:
        if a1 > b2 or a2 < b1:
            merged.append((a1, a2))
            a1, a2 = b1, b2
            continue
        a1, a2 = min(a1, b1), max(a2, b2)
    merged.append((a1, a2))

    return merged, beacons


def count_exclusive_positions(input, y):
    readings = parse_input(input)
    coverage, beacons = find_coverage(readings, y)
    return sum(abs(x2 - x1) + 1 for x1, x2 in coverage) - len(beacons)


def find_tuning_frequency(input, n):
    readings = parse_input(input)
    for y in range(0, n + 1):
        coverage, _ = find_coverage(readings, y)
        if len(coverage) < 2:
            continue
        return 4000000 * (coverage[0][1] + 1) + y


def part1(input: str):
    return count_exclusive_positions(input, 2000000)


def part2(input: str):
    return find_tuning_frequency(input, 4000000)


example = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""


def test_part1():
    assert count_exclusive_positions(example, 10) == 26


def test_part2():
    assert find_tuning_frequency(example, 20) == 56000011
