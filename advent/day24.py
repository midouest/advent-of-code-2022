from util.prelude import *


Valley = dict[Vec2D, str]
Prediction = tuple[int, int, str]
deltas = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}


def parse_input(input: str) -> tuple[Valley, Vec2D, Vec2D, Vec2D]:
    lines = input.strip().split("\n")
    x0 = lines[0].index(".") - 1
    xn = lines[-1].index(".") - 1
    valley = {
        (x, y): c
        for y, line in enumerate(lines[1:-1])
        for x, c in enumerate(line[1:-1])
        if c != "."
    }
    w, h = len(lines[0][1:-1]), len(lines[1:-1])
    return valley, (w, h), (x0, -1), (xn, h)


@dataclass
class Blizzard:
    data: dict[Vec2D : list[Prediction]]
    size: Vec2D

    def clear(self, coord: Vec2D, t: int) -> bool:
        return all(t % div != rem for div, rem, _ in self.data[coord])

    def debug(self, coord: Vec2D, t: int) -> str:
        return "".join([c for div, rem, c in self.data[coord] if t % div == rem])

    def dump(self, t: int) -> list[str]:
        w, h = self.size
        lines = []
        for y in range(h):
            line = ""
            for x in range(w):
                bs = self.debug((x, y), t)
                c = "."
                if len(bs) == 1:
                    c = bs
                elif len(bs) > 9:
                    c = "*"
                elif len(bs) > 0:
                    c = str(len(bs))
                line += c
            lines.append(line)
        return lines

    def print(self, t: int):
        lines = self.dump(t)
        for line in lines:
            print(line)
        print("")


def predict(valley: Valley, size: Vec2D):
    w, h = size
    predictions = defaultdict(list)
    for start, c in valley.items():
        x0, y0 = start
        dx, dy = step = deltas[c]
        px, py = dx * w, dy * h
        tx, ty = (px - 1 if px else 0), (py - 1 if py else 0)
        period = abs(px or py)
        stop = (tx + x0, ty + y0)
        for t, (x, y) in enumerate(irange_2d(start, stop, step)):
            x %= w
            y %= h
            predictions[(x, y)].append((period, t, c))
    return Blizzard(predictions, size)


def min_time(model: Blizzard, size: Vec2D, start: Vec2D, stop: Vec2D):
    w, h = size

    state = (0, start)
    frontier = deque([(state)])
    visited = set([state])

    while frontier:
        t, curr_pos = frontier.popleft()
        if curr_pos == stop:
            return t

        next_t = t + 1
        for delta in [(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)]:
            x, y = next_pos = add_2d(curr_pos, delta)
            next_state = (next_t, next_pos)
            if (
                next_state not in visited
                and x >= 0
                and x < w
                and (y >= 0 or next_pos == start)
                and (y < h or next_pos == stop)
                and model.clear(next_pos, next_t)
            ):
                frontier.append(next_state)
                visited.add(next_state)


def part1(input: str):
    valley, size, start, stop = parse_input(input)
    model = predict(valley, size)
    return min_time(model, size, start, stop)


def part2(input: str):
    raise NotImplementedError()


example = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""


small_example = """#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
"""


def test_small_example():
    valley, size, _, _ = parse_input(small_example)
    model = predict(valley, size)

    assert model.dump(0) == [
        ".....",
        ">....",
        ".....",
        "...v.",
        ".....",
    ]

    assert model.dump(1) == [
        ".....",
        ".>...",
        ".....",
        ".....",
        "...v.",
    ]

    assert model.dump(2) == [
        "...v.",
        "..>..",
        ".....",
        ".....",
        ".....",
    ]

    assert model.dump(3) == [
        ".....",
        "...2.",
        ".....",
        ".....",
        ".....",
    ]

    assert model.dump(4) == [
        ".....",
        "....>",
        "...v.",
        ".....",
        ".....",
    ]

    assert model.dump(5) == [
        ".....",
        ">....",
        ".....",
        "...v.",
        ".....",
    ]


def test_part1():
    assert part1(example) == 18


def test_part2():
    assert part2(example) == 0
