from util.prelude import *


Cost = tuple[int, int, int]
Blueprint = tuple[Cost, Cost, Cost, Cost]
pattern = r"Blueprint \d+: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."


def parse_input(input: str) -> list[Blueprint]:
    blueprints = []
    for matches in findall(pattern, input):
        a1, b1, c1, c2, d1, d2 = map(int, matches)
        blueprint = ((a1, 0, 0), (b1, 0, 0), (c1, c2, 0), (d1, 0, d2))
        blueprints.append(blueprint)
    return blueprints


@dataclass(eq=True, frozen=True, order=True)
class State:
    time: int = 24
    materials: tuple = (0, 0, 0, 0)
    robots: tuple = (1, 0, 0, 0)

    def buildable_times(self, bp):
        return (
            max(
                0 if m >= c else ceil((c - m) / r) if r > 0 else inf
                for m, c, r in zip(self.materials, costs, self.robots)
            )
            for costs in bp
        )

    def build(self, i, bp, dt):
        dt += 1
        materials = tuple(
            m + (dt * r) - c
            for m, c, r in zip(self.materials, bp[i] + (0,), self.robots)
        )
        robots = self.robots[:i] + (self.robots[i] + 1,) + self.robots[i + 1 :]
        return State(self.time - dt, materials, robots)


@dataclass
class GeodeSearch(AStarSearch[State]):
    start: State
    stop: int
    blueprint: Blueprint

    def initial(self):
        return [self.start]

    def goal(self, current: State):
        return current.robots[3] == self.start.robots[3] + self.stop

    def neighbors(self, current: State) -> Iterable[State]:
        buildable_times = current.buildable_times(self.blueprint)
        for i, dt in enumerate(buildable_times):
            if dt < current.time:
                yield current.build(i, self.blueprint, dt)

    def distance(self, current: State, neighbor: State) -> int:
        return current.time - neighbor.time


def maximize_geodes(blueprint):
    best = 0
    for i in count(start=1):
        path = GeodeSearch(State(), i, blueprint).djikstra()
        if not path:
            break
        state = path[-1]
        geodes = state.materials[3] + state.time * state.robots[3]
        if geodes < best:
            break
        best = geodes
    return best


def part1(input: str):
    return sum(
        i * maximize_geodes(blueprint)
        for i, blueprint in tqdm(list(enumerate(parse_input(input), 1)))
    )


def part2(input: str):
    raise NotImplementedError()


example = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""


def test_maximize():
    assert maximize_geodes(((4, 0, 0), (2, 0, 0), (3, 14, 0), (2, 0, 7))) == 9
    assert maximize_geodes(((2, 0, 0), (3, 0, 0), (3, 8, 0), (3, 0, 12))) == 12


def test_part1():
    assert part1(example) == 33


def test_part2():
    assert part2(example) == 0
