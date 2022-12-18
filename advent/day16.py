import re
from dataclasses import dataclass, field
from util.search import Search


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


def start_valves(valves: dict[str, Valve]):
    return (
        valve.name for valve in valves.values() if valve.rate > 0 or valve.name == "AA"
    )


def stop_valves(valves: dict[str, Valve], start_valve: str):
    return (
        valve.name
        for valve in valves.values()
        if valve.rate > 0 and valve.name != start_valve
    )


def find_paths(valves: dict[str, Valve]) -> dict[tuple[str, str], int]:
    distances = {}
    for start in start_valves(valves):
        for stop in stop_valves(valves, start):
            path = ValveSearch(valves, start, stop).bfs()
            distances[(start, stop)] = len(path) - 1
    return distances


pattern = r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (\w+)(?:, (\w+))?(?:, (\w+))?(?:, (\w+))?(?:, (\w+))?"


def parse_input(input: str):
    return {
        v0: Valve(v0, int(rate), [v for v in [v1, v2, v3, v4, v5] if v])
        for v0, rate, v1, v2, v3, v4, v5 in re.findall(pattern, input)
    }


@dataclass
class State:
    start: str = "AA"
    pressure: int = 0
    time: int = 30
    opened: set[str] = field(default_factory=set)


def part1(input: str):
    valves = parse_input(input)
    distances = find_paths(valves)
    stops = [valve.name for valve in valves.values() if valve.rate > 0]
    frontier = [State()]

    totals = []
    while frontier:
        state = frontier.pop()
        neighbors = []
        for stop in stops:
            if stop in state.opened:
                continue

            distance = distances[(state.start, stop)]
            if distance > state.time + 1:
                continue

            rate = valves[stop].rate
            time = state.time - (distance + 1)
            pressure = time * rate
            neighbors.append(
                State(stop, state.pressure + pressure, time, state.opened | set([stop]))
            )

        if not neighbors:
            totals.append(state.pressure)
        else:
            frontier.extend(neighbors)

    return max(totals)


def part2(input: str):
    raise NotImplementedError()


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