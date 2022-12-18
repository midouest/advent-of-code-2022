from argparse import ArgumentParser
from abc import ABC, abstractmethod


class Command(ABC):
    name: str
    description: str

    @abstractmethod
    def add_arguments(self, parser: ArgumentParser):
        raise NotImplementedError()

    @abstractmethod
    def exec(self, *args, **kwargs):
        raise NotImplementedError()
