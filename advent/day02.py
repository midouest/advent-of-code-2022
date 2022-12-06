lookup_p1 = {
    "X": {
        "C": 6,
        "B": 0,
        "A": 3,
    },
    "Y": {
        "A": 6,
        "B": 3,
        "C": 0,
    },
    "Z": {
        "B": 6,
        "C": 3,
        "A": 0,
    },
}

offset_p1 = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}


def calc_round_score_p1(round):
    them = round[0]
    us = round[2]
    return lookup_p1[us][them] + offset_p1[us]


lookup_p2 = {
    "X": {
        "A": 3,
        "B": 1,
        "C": 2,
    },
    "Y": {
        "A": 1,
        "B": 2,
        "C": 3,
    },
    "Z": {
        "A": 2,
        "B": 3,
        "C": 1,
    },
}

offset_p2 = {
    "X": 0,
    "Y": 3,
    "Z": 6,
}


def calc_round_score_p2(round):
    them = round[0]
    outcome = round[2]
    return lookup_p2[outcome][them] + offset_p2[outcome]


def calc_total_score(strategy_guide, score_strategy):
    return sum([score_strategy(round) for round in strategy_guide.strip().split("\n")])


def part1(input):
    return calc_total_score(input, calc_round_score_p1)


def part2(input):
    return calc_total_score(input, calc_round_score_p2)


example = """A Y
B X
C Z
"""


def test_example_p1():
    assert part1(example) == 15


def test_example_p2():
    assert part2(example) == 12
