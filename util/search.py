import math
import heapq
from abc import ABC, abstractmethod
from typing import TypeVar, Hashable, Callable, Iterable, Generic
from collections import deque, defaultdict


Node = TypeVar("Node", bound=Hashable)


class Path(Generic[Node]):
    def __init__(self, nodes: list[Node], visited: set[Node]):
        self.nodes = nodes
        self.visited = visited

    def __len__(self):
        return len(self.nodes)

    def __iter__(self):
        return iter(self.nodes)

    def __reversed__(self):
        return reversed(self.nodes)

    def __contains__(self, item):
        return item in self.nodes

    def __getitem__(self, key):
        return self.nodes[key]


class Search(Generic[Node], ABC):
    @abstractmethod
    def initial(self) -> Iterable[Node]:
        raise NotImplementedError()

    @abstractmethod
    def neighbors(self, node: Node) -> Iterable[Node]:
        raise NotImplementedError()

    @abstractmethod
    def goal(self, node: Node) -> bool:
        raise NotImplementedError()

    def reconstruct_path(
        self,
        current: Node,
        parents: dict[Node, Node],
    ) -> list[Node]:
        path = [current]
        while current in parents:
            current = parents[current]
            path.append(current)
        path.reverse()
        return path

    def search(self, take: Callable[[deque[Node]], Node]) -> Path[Node] | None:
        frontier: deque[Node] = deque(self.initial())
        visited: set[Node] = set(frontier)
        parents: dict[Node, Node] = {}

        while frontier:
            current = take(frontier)
            if self.goal(current):
                return Path(self.reconstruct_path(current, parents), visited)

            for neighbor in self.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parents[neighbor] = current
                    frontier.append(neighbor)

        return None

    def bfs(self) -> Path[Node] | None:
        return self.search(lambda frontier: frontier.popleft())

    def dfs(self) -> Path[Node] | None:
        return self.search(lambda frontier: frontier.pop())


class AStarSearch(Search[Node]):
    def initial_distance(self, node: Node) -> int:
        return 0

    @abstractmethod
    def distance(self, current: Node, neighbor: Node) -> int:
        raise NotImplementedError()

    @abstractmethod
    def heuristic(self, node: Node) -> int:
        raise NotImplementedError()

    def astar(self) -> Path[Node] | None:
        initial = self.initial()

        g_score: dict[Node, float] = defaultdict(lambda: math.inf)
        f_score: dict[Node, float] = defaultdict(lambda: math.inf)
        for node in initial:
            g_score[node] = self.initial_distance(node)
            f_score[node] = self.heuristic(node)

        open_set: set[Node] = set(initial)
        open_set_priorities: list[tuple[int, Node]] = [(0, node) for node in initial]
        parents: dict[Node, Node] = {}

        while open_set_priorities:
            _, current = heapq.heappop(open_set_priorities)
            open_set.remove(current)

            if self.goal(current):
                return Path(
                    self.reconstruct_path(current, parents), set(g_score.keys())
                )

            for neighbor in self.neighbors(current):
                tentative_g_score = g_score[current] + self.distance(current, neighbor)
                if tentative_g_score < g_score[neighbor]:
                    parents[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f = tentative_g_score + self.heuristic(neighbor)
                    f_score[neighbor] = f

                    if neighbor not in open_set:
                        open_set.add(neighbor)
                        heapq.heappush(open_set_priorities, (f, neighbor))  # type: ignore

        return None


class DjikstraSearch(AStarSearch[Node]):
    def heuristic(self, node: Node) -> int:
        return 0

    def djikstra(self) -> Path[Node]:
        return self.astar()
