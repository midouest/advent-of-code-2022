from util.prelude import *


EMPTY = " "


def parse_input(input: str) -> tuple[list[str], list[int | str]]:
    board_input, path_input = input.rstrip().split("\n\n")
    board = board_input.split("\n")

    path = [
        int(move) if move else turn
        for move, turn in findall(r"(\d+)|([LR])", path_input)
    ]
    return board, path


def wrap_flat(board):
    def find_wrap_y(x, y):
        for wy in range(len(board) - 1, y, -1):
            line = board[wy]
            if x < len(line) and line[x] != EMPTY:
                return wy

    def find_wrap_x(x, y):
        line = board[y]
        for wx in range(len(line) - 1, x, -1):
            if line[x] != EMPTY:
                return wx

    wrap_to = {}
    for y, line in enumerate(board):
        for x, c in enumerate(line):
            if c == EMPTY:
                continue
            py = y - 1
            if y == 0 or x >= len(board[py]) or board[py][x] == EMPTY:
                wy = find_wrap_y(x, y)
                wrap_to[(x, py, 0, -1)] = (x, wy, 0, -1)
                wrap_to[(x, wy + 1, 0, 1)] = (x, y, 0, 1)

            px = x - 1
            if x == 0 or line[px] == EMPTY:
                wx = find_wrap_x(x, y)
                wrap_to[(px, y, -1, 0)] = (wx, y, -1, 0)
                wrap_to[(wx + 1, y, 1, 0)] = (x, y, 1, 0)

    return wrap_to


@dataclass(eq=True, frozen=True)
class Side:
    p1: Vec2D
    p2: Vec2D
    normal: Vec2D
    delta: Vec2D


X_POS = (1, 0)
X_NEG = (-1, 0)
Y_POS = (0, 1)
Y_NEG = (0, -1)


def find_sides(board, size):
    x0, y0 = coord0 = initial = board[0].index("."), 0
    x1, y1 = coord1 = x0 + size - 1, y0
    sides = [Side(coord0, coord1, Y_NEG, X_POS)]
    corners = []
    max_y = len(board) - 1

    while coord1 != initial:
        if x0 == x1:
            if y1 > y0:  # pointing down
                neighbors = (
                    (-90, (x1 + 1, y1 + 1), (x1 + size, y1 + 1), Y_NEG, X_POS),
                    (0, (x1, y1 + 1), (x1, y1 + size), X_POS, Y_POS),
                    (90, (x1, y1), (x1 - size + 1, y1), Y_POS, X_NEG),
                )
            else:  # pointing up
                neighbors = (
                    (-90, (x1 - 1, y1 - 1), (x1 - size, y1 - 1), Y_POS, X_NEG),
                    (0, (x1, y1 - 1), (x1, y1 - size), X_NEG, Y_NEG),
                    (90, (x1, y1), (x1 + size - 1, y1), Y_NEG, X_POS),
                )
        elif y0 == y1:
            if x1 > x0:  # pointing right
                neighbors = (
                    (-90, (x1 + 1, y1 - 1), (x1 + 1, y1 - size), X_NEG, Y_NEG),
                    (0, (x1 + 1, y1), (x1 + size, y1), Y_NEG, X_POS),
                    (90, (x1, y1), (x1, y1 + size - 1), X_POS, Y_POS),
                )
            else:  # pointing left
                neighbors = (
                    (-90, (x1 - 1, y1 + 1), (x1 - 1, y1 + size), X_POS, Y_POS),
                    (0, (x1 - 1, y1), (x1 - size, y1), Y_POS, X_NEG),
                    (90, (x1, y1), (x1, y1 - size + 1), X_NEG, Y_NEG),
                )

        for corner, coord0, coord1, normal, delta in neighbors:
            (x0, y0), (x1, y1) = coord0, coord1
            if y0 < 0 or y1 < 0 or y0 > max_y or y1 > max_y:
                continue
            line0, line1 = board[y0], board[y1]
            if (
                x0 < 0
                or x0 > len(line0) - 1
                or line0[x0] == EMPTY
                or x1 < 0
                or x1 > len(line1) - 1
                or line1[x1] == EMPTY
            ):
                continue
            sides.append(Side(coord0, coord1, normal, delta))
            corners.append(corner)
            break

    return sides, corners


def wrap_box(board, size):
    wrap_to = {}
    sides, corners = find_sides(board, size)
    visited = set()

    def wrap_sides(a, b):
        wrap_a = irange_2d(a.p2, a.p1, invert_2d(a.delta))
        wrap_b = irange_2d(b.p1, b.p2, b.delta)
        for wa, wb in zip(wrap_a, wrap_b):
            wrap_to[add_2d(wa, a.normal) + a.normal] = wb + invert_2d(b.normal)
            wrap_to[add_2d(wb, b.normal) + b.normal] = wa + invert_2d(a.normal)
        visited.update([a, b])

    for i, (corner, (a, b)) in enumerate(zip(corners, pairwise(sides))):
        if corner != -90:
            continue
        wrap_sides(a, b)

        ai, bi = (i - 1) % len(sides), (i + 2) % len(sides)
        a, b = sides[ai], sides[bi]
        if a.normal == b.normal:
            wrap_sides(a, b)

    remaining = set(sides) - visited
    for a in remaining:
        if a in visited:
            continue
        i = sides.index(a)
        for j in [5, 7]:
            unvisited = {sides[(i - k) % len(sides)] for k in [-j, j]} - visited
            if unvisited:
                b = unvisited.pop()
                break
        wrap_sides(a, b)

    return wrap_to


deltas = ((1, 0), (0, 1), (-1, 0), (0, -1))


def follow_directions(board, wrap_to, path):
    x, y = board[0].index("."), 0
    dx, dy = 1, 0
    face = 0

    visited = {}
    for dir in path:
        if type(dir) == int:
            visited[(x, y)] = face
            for _ in range(dir):
                move = (x + dx, y + dy, dx, dy)
                nx, ny, ndx, ndy = wrap_to.get(move, move)
                if board[ny][nx] == "#":
                    break
                x, y, dx, dy = nx, ny, ndx, ndy
                face = deltas.index((dx, dy))
                visited[(x, y)] = face
        else:
            if dir == "L":
                face -= 1
            else:
                face += 1
            face %= len(deltas)
            dx, dy = deltas[face]

    return 1000 * (y + 1) + 4 * (x + 1) + face


def part1(input: str):
    board, path = parse_input(input)
    wrap_to = wrap_flat(board)
    return follow_directions(board, wrap_to, path)


def trace_path(input: str, size: int):
    board, path = parse_input(input)
    wrap_to = wrap_box(board, size)
    return follow_directions(board, wrap_to, path)


def part2(input: str):
    return trace_path(input, 50)


example = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""


def test_part1():
    assert part1(example) == 6032


def test_part2():
    assert trace_path(example, 4) == 5031
