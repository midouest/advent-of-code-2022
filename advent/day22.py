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


def find_sides(board, size):
    x0, y0 = coord0 = initial = board[0].index("."), 0
    x1, y1 = coord1 = x0 + size - 1, y0
    sides = [(coord0, coord1)]
    max_y = len(board) - 1

    while coord1 != initial:
        if x0 == x1:
            if y1 > y0:  # pointing down
                neighbors = (
                    ((x1 + 1, y1 + 1), (x1 + size, y1 + 1)),
                    ((x1, y1 + 1), (x1, y1 + size)),
                    ((x1, y1), (x1 - size + 1, y1)),
                )
            else:  # pointing up
                neighbors = (
                    ((x1 - 1, y1 - 1), (x1 - size, y1 - 1)),
                    ((x1, y1 - 1), (x1, y1 - size)),
                    ((x1, y1), (x1 + size - 1, y1)),
                )
        elif y0 == y1:
            if x1 > x0:  # pointing right
                neighbors = (
                    ((x1 + 1, y1 - 1), (x1 + 1, y1 - size)),
                    ((x1 + 1, y1), (x1 + size, y1)),
                    ((x1, y1), (x1, y1 + size - 1)),
                )
            else:  # pointing left
                neighbors = (
                    ((x1 - 1, y1 + 1), (x1 - 1, y1 + size)),
                    ((x1 - 1, y1), (x1 - size, y1)),
                    ((x1, y1), (x1, y1 - size + 1)),
                )

        for side in neighbors:
            (x0, y0), (x1, y1) = coord0, coord1 = side
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
            sides.append(side)
            break

    return sides


def wrap_box(board, size):
    wrap_to = {}
    sides = find_sides(board, size)
    return wrap_to


deltas = ((1, 0), (0, 1), (-1, 0), (0, -1))


def follow_directions(board, wrap_to, path):
    x, y = board[0].index("."), 0
    dx, dy = 1, 0
    face = 0

    for dir in path:
        if type(dir) == int:
            for _ in range(dir):
                move = (x + dx, y + dy, dx, dy)
                nx, ny, ndx, ndy = wrap_to.get(move, move)
                if board[ny][nx] == "#":
                    break
                x, y, dx, dy = nx, ny, ndx, ndy
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
