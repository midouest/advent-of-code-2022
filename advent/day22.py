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
                wrap_to[(x, py, 0, -1)] = (x, wy)
                wrap_to[(x, wy + 1, 0, 1)] = (x, y)

            px = x - 1
            if x == 0 or line[px] == EMPTY:
                wx = find_wrap_x(x, y)
                wrap_to[(px, y, -1, 0)] = (wx, y)
                wrap_to[(wx + 1, y, 1, 0)] = (x, y)

    return wrap_to


deltas = ((1, 0), (0, 1), (-1, 0), (0, -1))


def follow_directions(board, wrap_to, path):
    x, y = board[0].index("."), 0
    dx, dy = 1, 0
    face = 0

    for dir in path:
        if type(dir) == int:
            for _ in range(dir):
                move_to = (x + dx, y + dy)
                nx, ny = wrap_to.get(move_to + (dx, dy), move_to)
                if board[ny][nx] == "#":
                    break
                x, y = nx, ny
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


def part2(input: str):
    raise NotImplementedError()


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
    assert part2(example) == 5031
