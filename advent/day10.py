import re


class ClockCircuit:
    def __init__(self, delegate):
        self.x = 1
        self.cycle = 1
        self.delegate = delegate

    def eval(self, input):
        for v in re.findall(r"(?:addx|noop)(?: (-?\d+))?", input):
            self.step()
            if v:
                self.step()
                self.x += int(v)

    def step(self):
        self.delegate.during_cycle(self)
        self.cycle += 1


class SignalStrength:
    def __init__(self):
        self.next_cycle = 20
        self.total = 0

    def during_cycle(self, circuit):
        if circuit.cycle != self.next_cycle or self.next_cycle > 220:
            return

        self.total += circuit.cycle * circuit.x
        self.next_cycle += 40


def part1(input: str):
    signal_strength = SignalStrength()
    circuit = ClockCircuit(signal_strength)
    circuit.eval(input)
    return signal_strength.total


class CRT:
    def __init__(self):
        self.pixels = [["."] * 40 for _ in range(6)]

    def during_cycle(self, circuit):
        x = (circuit.cycle - 1) % 40
        sprite = [circuit.x + i for i in [-1, 0, 1]]
        if x not in sprite:
            return
        y = (circuit.cycle - 1) // 40
        self.pixels[y][x] = "#"


def part2(input: str):
    crt = CRT()
    circuit = ClockCircuit(crt)
    circuit.eval(input)
    return ["".join(row) for row in crt.pixels]


example = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""


def test_part1():
    assert part1(example) == 13140


expected = [
    "##..##..##..##..##..##..##..##..##..##..",
    "###...###...###...###...###...###...###.",
    "####....####....####....####....####....",
    "#####.....#####.....#####.....#####.....",
    "######......######......######......####",
    "#######.......#######.......#######.....",
]


def test_part2():
    assert part2(example) == expected


def encode(output: list[str]) -> str:
    pixels = "".join(output)
    program = []
    x = 1
    i = 2
    while i < 240:
        pixel1 = pixels[i]
        pixel2 = pixels[i + 1] if i < 239 else None
        diff = i % 40 - x
        in_sprite = abs(diff) < 2

        if pixel1 == "#" and not in_sprite:
            if pixel2 == "#":
                program.append(f"addx {diff}")
            else:
                diff -= 1
                program.append(f"addx {diff}")
            x += diff
            i += 2
        elif pixel1 == "." and in_sprite:
            if pixel2 == ".":
                diff -= 2
                program.append(f"addx {diff}")
            else:
                diff += 2
                program.append(f"addx {diff}")
            x += diff
            i += 2
        else:
            program.append("noop")
            i += 1

    return "\n".join(program)


def test_encode_example():
    assert part2(encode(expected)) == expected


def test_encode_zzzzzz():
    output = [
        "####.####.####.####.####.####.####.####.",
        "...#....#....#....#....#....#....#....#.",
        "..#....#....#....#....#....#....#....#..",
        ".#....#....#....#....#....#....#....#...",
        "#....#....#....#....#....#....#....#....",
        "####.####.####.####.####.####.####.###..",  # TODO: second-to-last position should be #
    ]
    assert part2(encode(output)) == output
