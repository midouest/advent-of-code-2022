from importlib import import_module
from util import puzzle


def command(day, part):
    days = range(1, 26) if day == 0 else [day]
    parts = range(1, 3) if part == 0 else [part]

    for day in days:
        try:
            day_suffix = puzzle.format_day_suffix(day)
            module_name = f"advent.day{day_suffix}"
            module = import_module(module_name)
        except:
            return

        puzzle_input = puzzle.read(module.__file__)

        print(f"day {day}")
        print("---")
        for part in parts:
            try:
                part_name = f"part{part}"
                part_func = getattr(module, part_name)
            except:
                return

            answer = part_func(puzzle_input)
            print(f"part {part} = {answer}")
        print("")
