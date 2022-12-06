import requests
import pathlib
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
        with open(".session") as session_file:
            session = session_file.read().strip()

        cookies = {"session": session}
        response = requests.get(
            f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies
        )

        day_suffix = puzzle.format_day_suffix(day)
        base_dir = pathlib.Path("advent")
        input_path = base_dir / f"day{day_suffix}.txt"
        with open(input_path, "w") as input_file:
            input_file.write(response.text)

        solution_path = base_dir / f"day{day_suffix}.py"
        with open(solution_path, "w") as solution_file:
            solution_file.write(template)
