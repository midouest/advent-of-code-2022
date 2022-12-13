import math
import heapq
from abc import ABC, abstractmethod
from typing import TypeVar, Hashable, Callable, Iterable
from collections import deque, defaultdict


Node = TypeVar("Node", bound=Hashable)
Path = list[Node]


class PathNotFound(Exception):
    ...


class Search(ABC):
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
    ) -> Path:
        path = [current]
        while current in parents:
            current = parents[current]
            path.append(current)
        path.reverse()
        return path

    def search(self, take: Callable[[deque], Node]) -> Path:
        frontier: deque[Node] = deque(self.initial())
        visited: set[Node] = set(frontier)
        parents: dict[Node, Node] = {}

        while frontier:
            current = take(frontier)
            if self.goal(current):
                return self.reconstruct_path(current, parents)

            for neighbor in self.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parents[neighbor] = current
                    frontier.append(neighbor)

        raise PathNotFound()

    def bfs(self) -> Path:
        return self.search(lambda frontier: frontier.popleft())

    def dfs(self) -> Path:
        return self.search(lambda frontier: frontier.pop())


class AStarSearch(Search):
    @abstractmethod
    def distance(self, current: Node, neighbor: Node) -> int:
        raise NotImplementedError()

    @abstractmethod
    def heuristic(self, node: Node) -> int:
        raise NotImplementedError()

    def astar(self) -> Path:
        initial = self.initial()

        g_score: dict[Node, float] = defaultdict(lambda: math.inf)
        f_score: dict[Node, float] = defaultdict(lambda: math.inf)
        for node in initial:
            g_score[node] = 0
            f_score[node] = self.heuristic(node)

        open_set: set[Node] = set(initial)
        open_set_priorities: list[tuple[int, Node]] = [(0, node) for node in initial]
        parents: dict[Node, Node] = {}

        while open_set_priorities:
            _, current = heapq.heappop(open_set_priorities)
            open_set.remove(current)

            if self.goal(current):
                return self.reconstruct_path(current, parents)

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

        raise PathNotFound()


class DjikstraSearch(AStarSearch):
    def heuristic(self, node: Node) -> int:
        return 0

    def djikstra(self) -> Path:
        return self.astar()
