from util.prelude import *


def decode(snafu: str) -> int:
    s2n = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
    return sum(s2n[c] * pow(5, i) for i, c in enumerate(reversed(snafu)))


def encode(n: int) -> str:
    s = ""
    acc = n
    for i in count():
        div = pow(5, i)
        acc += 2 * div
        idx = acc // div % 5
        dig = "=-012"[idx]
        s = dig + s
        if decode(s) == n:
            break
    return s


def part1(input: str):
    lines = input.strip().split("\n")
    total = sum(decode(line) for line in lines)
    return encode(total)


example = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""


def test_part1():
    assert part1(example) == "2=-1=0"
