import re
from util.iterator import chunks


def parse_stacks(text):
    num_stacks = int(re.findall(r"(?: (\d) )[ \n]", text)[-1])
    stacks = []
    for i in range(num_stacks):
        stacks.append([])

    crates = list(reversed(re.findall(r"(?:   |\[([A-Z])\])[ \n]", text)))
    for reverse_row in chunks(crates, num_stacks):
        row = reversed(reverse_row)
        for i, crate in enumerate(row):
            if crate:
                stacks[i].append(crate)

    return stacks


def test_parse_stacks():
    assert parse_stacks(example) == [["Z", "N"], ["M", "C", "D"], ["P"]]


def crate_mover_9000(n, src, dst):
    for _ in range(n):
        dst.append(src.pop())


def crate_mover_9001(n, src, dst):
    crates = src[-n:]
    del src[-n:]
    dst.extend(crates)


def execute_instructions(text, crane):
    stacks = parse_stacks(text)

    for matches in re.findall(r"move (\d+) from (\d+) to (\d+)", text):
        n, src, dst = map(int, matches)
        src_stack = stacks[src - 1]
        dst_stack = stacks[dst - 1]
        crane(n, src_stack, dst_stack)

    return "".join(stack[-1] for stack in stacks)


def part1(input):
    return execute_instructions(input, crate_mover_9000)


def part2(input):
    return execute_instructions(input, crate_mover_9001)


# fmt: off
example = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
# fmt: on


def test_part1():
    assert part1(example) == "CMZ"


def test_part2():
    assert part2(example) == "MCD"
