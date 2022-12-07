from argparse import ArgumentParser
from commands.base import Command
from util import puzzle


class RunCommand(Command):
    name = "run"

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "day",
            type=int,
            nargs="?",
            choices=range(1, 26),
            default=0,
            help="The day to run",
        )
        parser.add_argument(
            "part",
            type=int,
            nargs="?",
            choices=(
                1,
                2,
            ),
            default=0,
            help="The part to run",
        )
        parser.add_argument(
            "--submit",
            action="store_true",
            help="Submit the answer for the last part executed",
        )

    def exec(self, day: int, part: int, submit: bool):
        days = range(1, 26) if day == 0 else [day]
        parts = range(1, 3) if part == 0 else [part]

        for day in days:
            try:
                module = puzzle.load_module(day)
            except:
                return

            puzzle_input = puzzle.read(module.__file__)

            print(f"day {day}")
            print("---")
            for part in parts:
                try:
                    part_func = puzzle.get_part_function(module, part)
                except:
                    return

                answer = part_func(puzzle_input)
                print(f"part {part} = {answer}")

        print("")

        if submit:
            print(f"Submitting answer for day {day}, part {part}...")
            response = puzzle.submit_answer(day, part, answer)
            print("> " + response)

        print("")
