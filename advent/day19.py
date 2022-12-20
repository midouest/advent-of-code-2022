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
    time: int
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


def maximize_geodes(blueprint, time):
    frontier = [State(time)]
    visited = set(frontier)

    build_limits = [max(costs) for costs in zip(*blueprint)]
    bests = defaultdict(int)

    best = 0
    while frontier:
        state = frontier.pop()

        geodes = state.materials[3]
        best_at_time = bests[state.time]
        if geodes > best_at_time:
            bests[state.time] = geodes
        elif best_at_time > geodes + 2:
            continue

        neighbors = []
        buildable_times = state.buildable_times(blueprint)
        for i, dt in enumerate(buildable_times):
            if (
                dt < state.time
                and all(r <= limit for r, limit in zip(state.robots[:3], build_limits))
                and (
                    state.time >= time // 3
                    or all(
                        r >= expected for r, expected in zip(state.robots, (1, 1, 1, 0))
                    )
                )
            ):
                neighbor = state.build(i, blueprint, dt)
                neighbors.append(neighbor)
                visited.add(neighbor)

        if neighbors:
            frontier.extend(neighbors)
        else:
            best = max(best, geodes + state.time * state.robots[3])

    return best


def part1(input: str):
    return sum(
        i * maximize_geodes(blueprint, 24)
        for i, blueprint in tqdm(list(enumerate(parse_input(input), 1)))
    )


def part2(input: str):
    blueprints = parse_input(input)
    return prod(maximize_geodes(bp, 32) for bp in tqdm(blueprints[:3]))


example = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""


def test_part1():
    assert part1(example) == 33


def test_part2():
    assert part2(example) == 56 * 62
