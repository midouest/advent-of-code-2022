from util.prelude import *


@dataclass
class Valve:
    name: str
    rate: int
    neighbors: list[str]


@dataclass
class ValveSearch(Search):
    valves: dict[str, Valve]
    start: str
    stop: str

    def initial(self):
        return [self.start]

    def neighbors(self, node: str):
        return self.valves[node].neighbors

    def goal(self, node: str):
        return node == self.stop


def find_paths(valves: dict[str, Valve]) -> dict[tuple[str, str], int]:
    distances = {}
    for start, stop in permutations(valves.values(), 2):
        if start.name != "AA" and start.rate == 0 or stop.rate == 0:
            continue
        path = ValveSearch(valves, start.name, stop.name).bfs()
        distances[(start.name, stop.name)] = len(path) - 1
    return distances


pattern = r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (\w+)(?:, (\w+))?(?:, (\w+))?(?:, (\w+))?(?:, (\w+))?"


def parse_input(input: str):
    return {
        v0: Valve(v0, int(rate), [v for v in [v1, v2, v3, v4, v5] if v])
        for v0, rate, v1, v2, v3, v4, v5 in findall(pattern, input)
    }


@dataclass
class State:
    time: int
    start: str = "AA"
    pressure: int = 0
    opened: tuple = field(default_factory=tuple)

    def __hash__(self) -> int:
        return hash(self.opened)


def explore(input: str, t0: int):
    valves = parse_input(input)
    distances = find_paths(valves)
    stops = [valve.name for valve in valves.values() if valve.rate > 0]
    frontier = [State(t0)]
    visited = set(frontier)

    while frontier:
        state = frontier.pop()
        for stop in stops:
            if stop in state.opened:
                continue

            distance = distances[(state.start, stop)]
            if distance > state.time + 1:
                continue

            rate = valves[stop].rate
            time = state.time - (distance + 1)
            pressure = state.pressure + time * rate
            opened = state.opened + (stop,)
            neighbor = State(time, stop, pressure, opened)
            frontier.append(neighbor)
            visited.add(neighbor)

    return visited


def part1(input: str):
    return max(map(attrgetter("pressure"), explore(input, 30)))


def part2(input: str):
    states = explore(input, 26)

    candidates = {}
    for state in states:
        key = tuple(sorted(state.opened))
        other = candidates.get(key, state)
        candidates[key] = max(state, other, key=attrgetter("pressure"))

    best = 0
    for you, elph in permutations(candidates.values(), 2):
        if set(you.opened).isdisjoint(elph.opened):
            best = max(best, you.pressure + elph.pressure)

    return best


example = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""


def test_part1():
    assert part1(example) == 1651


def test_part2():
    assert part2(example) == 1707
