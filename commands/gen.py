import requests
import pathlib
from util import puzzle


template = """def part1(input: str):
    raise NotImplementedError()


def part2(input: str):
    raise NotImplementedError()
"""


def command(day):
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
