from argparse import ArgumentParser
from commands.base import Command
from util import puzzle


template = '''from util.prelude import *


def part1(input: str):
    raise NotImplementedError()


def part2(input: str):
    raise NotImplementedError()


example = """
"""


def test_part1():
    assert part1(example) == 0


def test_part2():
    assert part2(example) == 0
'''


class G(Command):
    name = "g"
    description = "generate input and solution files for the given day"

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "day",
            type=int,
            choices=range(1, 26),
            help="the day to generate",
        )
        parser.add_argument(
            "-i",
            "--input",
            action="store_true",
            help="only download the puzzle input",
        )

    def exec(self, day: int, input: bool):
        puzzle_input = puzzle.fetch_input(day)
        puzzle.write_input(day, puzzle_input)
        if input:
            return

        puzzle.write_solution(day, template)
