def clean_input(input):
    return [[int(c) for c in line] for line in input.strip().split("\n")]


def find_visible_x(lines, start, stop, step):
    found = set()
    for y in range(1, len(lines) - 1):
        line = lines[y]
        prev = line[start - step]
        for x in range(start, stop, step):
            tree = line[x]
            if tree <= prev:
                continue
            found.add((x, y))
            prev = tree
    return found


def find_visible_y(lines, start, stop, step):
    width = len(lines[0])
    found = set()
    for x in range(1, width - 1):
        prev = lines[start - step][x]
        for y in range(start, stop, step):
            tree = lines[y][x]
            if tree <= prev:
                continue
            found.add((x, y))
            prev = tree
    return found


def part1(input: str):
    lines = clean_input(input)
    w = len(lines[0])
    h = len(lines)

    left = find_visible_x(lines, 1, w - 1, 1)
    right = find_visible_x(lines, w - 2, 0, -1)
    top = find_visible_y(lines, 1, h - 1, 1)
    bottom = find_visible_y(lines, h - 2, 0, -1)
    found = left | right | top | bottom

    return len(found) + 2 * (w + h - 2)


def find_visible_x_along(lines, y, start, stop, step):
    found = set()
    line = lines[y]
    prev = line[start - step]
    for x in range(start, stop, step):
        tree = line[x]
        found.add((x, y))
        if tree >= prev:
            break
    return found


def find_visible_y_along(lines, x, start, stop, step):
    found = set()
    prev = lines[start - step][x]
    for y in range(start, stop, step):
        tree = lines[y][x]
        found.add((x, y))
        if tree >= prev:
            break
    return found


def scenic_score(lines, x, y):
    w = len(lines[0])
    h = len(lines)

    right = find_visible_x_along(lines, y, x + 1, w, 1)
    left = find_visible_x_along(lines, y, x - 1, -1, -1)
    bottom = find_visible_y_along(lines, x, y + 1, h, 1)
    top = find_visible_y_along(lines, x, y - 1, -1, -1)
    return len(left) * len(right) * len(top) * len(bottom)


def part2(input: str):
    lines = clean_input(input)
    w = len(lines[0])
    h = len(lines)
    scores = [
        scenic_score(lines, x, y) for y in range(1, h - 1) for x in range(1, w - 1)
    ]
    return max(scores)
    # 108 too low


example = """30373
25512
65332
33549
35390
"""


def test_part1():
    assert part1(example) == 21


def test_part2():
    lines = clean_input(example)
    assert scenic_score(lines, 2, 1) == 4
    assert scenic_score(lines, 2, 3) == 8
    assert part2(example) == 8
