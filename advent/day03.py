def find_misplaced_item(rucksack):
    half = len(rucksack) // 2
    left = set(rucksack[:half])
    right = set(rucksack[half:])
    intersection = left & right
    return intersection.pop()


def priority(item):
    code = ord(item)
    if item.isupper():
        return code - 38
    return code - 96


def sum_misplaced_priorities(rucksacks):
    return sum(
        priority(find_misplaced_item(rucksack))
        for rucksack in rucksacks.strip().split("\n")
    )


def chunks(items, n):
    for i in range(0, len(items), n):
        yield items[i : i + n]


def find_badge(group):
    intersection = set(group[0]) & set(group[1]) & set(group[2])
    return intersection.pop()


def sum_badge_priorities(rucksacks):
    return sum(
        priority(find_badge(group))
        for group in chunks(rucksacks.strip().split("\n"), 3)
    )


def part1(input):
    return sum_misplaced_priorities(input)


def part2(input):
    return sum_badge_priorities(input)


example = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


def test_part1():
    assert part1(example) == 157


def test_part2():
    assert part2(example) == 70
