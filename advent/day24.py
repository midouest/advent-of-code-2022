from util.prelude import *


Valley = dict[Vec2D, str]


def parse_input(input: str) -> tuple[Valley, Vec2D, Vec2D, Vec2D]:
    lines = input.strip().split("\n")
    x_start = lines[0].index(".")
    x_goal = lines[-1].index(".")
    valley = {
        (x, y): c
        for y, line in enumerate(lines[1:-1])
        for x, c in enumerate(line[1:-1])
        if c != "."
    }
    w, h = len(lines[0][1:-1]), len(lines[1:-1])
    return valley, (w, h), (x_start, -1), (x_goal, h)


def tick(prev_valley: Valley, size: Vec2D) -> Valley:
    w, h = size
    next_valley = defaultdict(str)
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            blizzards = prev_valley.get((x, y))
            if not blizzards:
                continue
            for c in blizzards:
                match c:
                    case "^":
                        y = (y - 1) % h
                    case "v":
                        y = (y + 1) % h
                    case "<":
                        x = (x - 1) % w
                    case ">":
                        x = (x + 1) % w
                next_valley[(x, y)] += c
    return dict(next_valley)


def find_path(initial: Valley, size: Vec2D, start: Vec2D, finish: Vec2D):
    memo = [initial]
    w, h = size

    state = (0, start)
    frontier = deque([(state)])
    visited = set([state])

    while frontier:
        t, prev_pos = frontier.popleft()
        t += 1
        if t >= len(memo):
            valley = tick(memo[-1], size)
            memo.append(valley)
        else:
            valley = memo[t]

        for delta in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            x, y = next_pos = add_2d(prev_pos, delta)
            next_state = (t, next_pos)
            if (
                next_state not in visited
                and x >= 0
                and x < w
                and y >= 0
                and (y < h or next_pos == finish)
                and next_pos not in valley
            ):
                frontier.append(next_state)
                visited.add(next_state)

        if (t - 1, prev_pos) not in visited and prev_pos not in valley:
            next_state = (t, prev_pos)
            frontier.append(next_state)
            visited.add(next_state)


def part1(input: str):
    valley, size, start, finish = parse_input(example)
    find_path(valley, size, start, finish)


def part2(input: str):
    raise NotImplementedError()


example = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""


def test_part1():
    assert part1(example) == 18


def test_part2():
    assert part2(example) == 0
