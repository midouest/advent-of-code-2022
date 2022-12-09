import re
from dataclasses import dataclass, field

pattern = r"(?:\$ (?:cd (/|\.\.|\w+))|dir (\w+)|(\d+) ([a-z\.]+))"


@dataclass(unsafe_hash=True)
class Dir:
    size: int | None = None
    files: dict = field(default_factory=dict)

    def total_size(self) -> int:
        if self.size is not None:
            return self.size

        size = sum(file_size(file) for file in self.files.values())
        self.size = size
        return size

    def dirs(self):
        return filter(lambda file: type(file) == Dir, self.files.values())


def file_size(file: Dir | int) -> int:
    return file if type(file) == int else file.total_size()


def find_pwd(root: Dir, path: list) -> Dir:
    pwd = root
    for dir in path:
        pwd = pwd.files[dir]
    return pwd


def build_root(input: str) -> Dir:
    path = []
    root = Dir()
    pwd = root

    for cd, dir, size, file in re.findall(pattern, input):
        if cd:
            if cd == "..":
                path.pop()
                pwd = find_pwd(root, path)
            elif cd != "/":
                path.append(cd)
                pwd = find_pwd(root, path)
        elif dir:
            pwd.files[dir] = Dir()
        elif size and file:
            pwd.files[file] = int(size)

    return root


def part1(input: str):
    root = build_root(input)

    frontier = [root]
    total = 0
    while frontier:
        dir = frontier.pop()

        size = dir.total_size()
        if size <= 100000:
            total += size

        frontier.extend(dir.dirs())

    return total


def part2(input):
    root = build_root(input)
    disk_capacity = 70000000
    update_size = 30000000
    disk_usage = root.total_size()
    free_space = disk_capacity - disk_usage
    minimum_size = update_size - free_space

    frontier = [root]
    candidates = []
    while frontier:
        dir = frontier.pop()

        size = dir.total_size()
        if size >= minimum_size:
            candidates.append(dir)

        frontier.extend(dir.dirs())

    candidates.sort(key=Dir.total_size)
    return candidates[0].total_size()


example = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


def test_part1():
    assert part1(example) == 95437


def test_part2():
    assert part2(example) == 24933642
