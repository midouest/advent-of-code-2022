from util.prelude import *


def debug(file):
    print(list(map(itemgetter(1), file)))


def mix(input: str) -> list[int]:
    file = list(enumerate(map(int, input.strip().split("\n"))))
    size = len(file)

    for order in range(size):
        i, value = next(
            (index, value)
            for index, (original, value) in enumerate(file)
            if order == original
        )
        if value == 0:
            continue
        del file[i]

        j = i + value
        k = j
        if j <= 0:
            k = (j - 1) % len(file)
        elif j >= len(file):
            k = j % len(file)
        file.insert(k, (order, value))

    return [v for _, v in file]


def part1(input: str):
    file = mix(input)
    zero = file.index(0)
    size = len(file)
    return sum(file[(zero + i) % size] for i in [1000, 2000, 3000])


def part2(input: str):
    raise NotImplementedError()


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
    assert part2(example) == 0
