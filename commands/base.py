from argparse import ArgumentParser


class Command:
    name: str

    def add_arguments(self, parser: ArgumentParser):
        raise NotImplementedError()

    def exec(self, *args, **kwargs):
        raise NotImplementedError()
