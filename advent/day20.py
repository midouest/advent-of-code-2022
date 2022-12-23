from util.prelude import *


def parse_input(input: str):
    return map(int, input.strip().split("\n"))


def mix(file: list[tuple[int, int]]):
    original_size = len(file)

    for order in range(original_size):
        i, value = next(
            (index, value)
            for index, (original, value) in enumerate(file)
            if order == original
        )
        if value == 0:
            continue
        del file[i]
        new_size = len(file)

        j = i + value
        k = j % new_size
        file.insert(k, (order, value))

    return file


def mix_n(file: Iterable[int], n=1):
    file = list(enumerate(file))
    for _ in range(n):
        file = mix(file)
    return [v for _, v in file]


def decrypt(file: Iterable[int]):
    file = [n * 811589153 for n in file]
    return mix_n(file, 10)


def sum_grove_coordinates(file: list[int]):
    zero = file.index(0)
    size = len(file)
    coords = [file[(zero + i) % size] for i in [1000, 2000, 3000]]
    return sum(coords)


def part1(input: str):
    return sum_grove_coordinates(mix_n(parse_input(input)))


def part2(input: str):
    return sum_grove_coordinates(decrypt(parse_input(input)))


example = """1
2
-3
3
-2
0
4
"""


def test_part1():
    assert part1(example) == 3


def test_part2():
    assert part2(example) == 1623178306
