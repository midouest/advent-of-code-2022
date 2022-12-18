from argparse import ArgumentParser
from commands.base import Command
from util import puzzle


class R(Command):
    name = "r"
    description = "execute and submit solutions for given days and parts"

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "day",
            type=int,
            nargs="?",
            choices=range(1, 26),
            default=0,
            help="the day to run",
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
            help="the part to run",
        )
        parser.add_argument(
            "-s",
            "--submit",
            action="store_true",
            help="submit the answer for the given day and part",
        )

    def exec(self, day: int, part: int, submit: bool):
        days = range(1, 26) if day == 0 else [day]
        parts = range(1, 3) if part == 0 else [part]

        for d in days:
            try:
                module = puzzle.load_module(d)
            except:
                break

            puzzle_input = puzzle.read(module.__file__)

            print(f"day {d}")
            print("---")
            for p in parts:
                try:
                    part_func = puzzle.get_part_function(module, p)
                except:
                    break

                answer = part_func(puzzle_input)
                if type(answer) == list:
                    print(f"part {p} =")
                    for row in answer:
                        print(row)
                else:
                    print(f"part {p} = {answer}")

            print("")

        if not submit:
            return

        if day == 0 or part == 0:
            print("--submit requires an explicit day and part")
            return

        if type(answer) not in [int, str]:
            print("--submit only supports answers in integer or string format")
            return

        print(f"Submitting answer for day {day}, part {part}...")
        response = puzzle.submit_answer(day, part, answer)
        print("> " + response)
        print("")
