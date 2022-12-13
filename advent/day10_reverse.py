from advent.day10 import part2


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


example = [
    "##..##..##..##..##..##..##..##..##..##..",
    "###...###...###...###...###...###...###.",
    "####....####....####....####....####....",
    "#####.....#####.....#####.....#####.....",
    "######......######......######......####",
    "#######.......#######.......#######.....",
]


def test_encode_example():
    assert part2(encode(example)) == example
