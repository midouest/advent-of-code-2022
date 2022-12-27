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


@dataclass
class Side:
    normal: Vec3d
    up: Vec3d
    right: Vec3d


def fold_board(board, size):
    initial = (board[0].index("."), 0)
    sides = {initial: Side(normal=(0, 0, 1), up=(0, 1, 0), right=(1, 0, 0))}
    frontier = [initial]

    size_deltas = [(-size, 0), (size, 0), (0, size), (0, -size)]
    while frontier:
        x, y = current = frontier.pop()
        side = sides[current]
        for dx, dy in size_deltas:
            nx, ny = neighbor = x + dx, y + dy
            if neighbor in sides or ny < 0 or ny >= len(board):
                continue
            line = board[ny]
            if nx < 0 or nx >= len(line) or line[nx] == EMPTY:
                continue

            if dx < 0:
                rot = absolute_3d(side.up)
            elif dx > 0:
                rot = invert_3d(absolute_3d(side.up))
            elif dy > 0:
                rot = absolute_3d(side.right)
            elif dy < 0:
                rot = invert_3d(absolute_3d(side.right))

            normal = rotate_3d(side.normal, rot)
            up = rotate_3d(side.up, rot)
            right = rotate_3d(side.right, rot)
            sides[neighbor] = Side(normal, up, right)

            frontier.append(neighbor)

    return sides


def wrap_box(board, size):
    wrap_to = {}
    sides = fold_board(board, size)
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
