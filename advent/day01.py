def total_calories_per_elf(content):
    return [
        sum(int(food) for food in elf.split("\n") if food != "")
        for elf in content.split("\n\n")
    ]


def part1(input):
    return max(total_calories_per_elf(input))


def part2(input):
    totals = total_calories_per_elf(input)
    totals.sort(reverse=True)
    return sum(totals[:3])
