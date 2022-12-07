import pathlib
import requests
from typing import Any
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
