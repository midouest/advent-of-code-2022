import pathlib


def input_path(filename: str) -> pathlib.Path:
    return pathlib.Path(filename).with_suffix(".txt")


def read(filename: str) -> str:
    path = input_path(filename)
    with open(path) as f:
        return f.read()


def format_day_suffix(day: int) -> str:
    return str(day).zfill(2)
