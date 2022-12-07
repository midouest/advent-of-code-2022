from argparse import ArgumentParser
from commands.base import Command
from util import puzzle


template = """def part1(input: str):
    raise NotImplementedError()


def part2(input: str):
    raise NotImplementedError()
"""


class GenCommand(Command):
    name = "gen"

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "day", type=int, choices=range(1, 26), help="The day to generate"
        )

    def exec(self, day: int):
        puzzle_input = puzzle.fetch_input(day)
        puzzle.write_input(day, puzzle_input)
        puzzle.write_solution(day, template)
