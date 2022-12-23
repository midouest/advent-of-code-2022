import pathlib
import requests
from typing import Any
from importlib import import_module
from bs4 import BeautifulSoup


def input_path(filename: str) -> pathlib.Path:
    return pathlib.Path(filename).with_suffix(".txt")


def read(filename: str) -> str:
    path = input_path(filename)
    with open(path) as f:
        return f.read()


def format_day_suffix(day: int) -> str:
    return str(day).zfill(2)


def read_session_token() -> str:
    with open(".session") as session_file:
        return session_file.read().strip()


def prepare_cookies() -> dict:
    session = read_session_token()
    return {"session": session}


base_url = "https://adventofcode.com/2022/day"


def fetch_input(day: int) -> str:
    cookies = prepare_cookies()
    response = requests.get(f"{base_url}/{day}/input", cookies=cookies)
    return response.text


def submit_answer(day: int, part: int, answer: Any) -> str:
    cookies = prepare_cookies()
    form = {
        "level": part,
        "answer": answer,
    }
    response = requests.post(
        f"{base_url}/{day}/answer",
        cookies=cookies,
        data=form,
    )
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find("article").text


day_base_dir = "advent"
day_prefix = "day"


def load_module(day: int) -> object:
    day_suffix = format_day_suffix(day)
    module_name = f"{day_base_dir}.{day_prefix}{day_suffix}"
    return import_module(module_name)


def get_example(module: object) -> str:
    return getattr(module, "example")


def get_part_function(module: object, part: int) -> Any:
    part_name = f"part{part}"
    return getattr(module, part_name)


def puzzle_file_path(day: int, ext: str) -> pathlib.Path:
    day_suffix = format_day_suffix(day)
    base_dir = pathlib.Path(day_base_dir)
    return base_dir / f"{day_prefix}{day_suffix}.{ext}"


def write_input(day: int, input: str):
    input_path = puzzle_file_path(day, "txt")
    with open(input_path, "w") as input_file:
        input_file.write(input)


def write_solution(day: int, template: str):
    solution_path = puzzle_file_path(day, "py")
    with open(solution_path, "w") as solution_file:
        solution_file.write(template)
