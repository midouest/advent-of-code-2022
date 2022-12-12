import math
import heapq
from abc import ABC, abstractmethod
from typing import TypeVar, Hashable
from collections import deque, defaultdict


Node = TypeVar("Node")
NodeId = TypeVar("NodeId", bound=Hashable)


class PathNotFound(Exception):
    ...


class Search(ABC):
    @abstractmethod
    def initial(self) -> Node:
        raise NotImplementedError()

    def identity(self, node: Node) -> NodeId:
        return node

    @abstractmethod
    def neighbors(self, node: Node) -> list[Node]:
        raise NotImplementedError()

    @abstractmethod
    def goal(self, node: Node) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def distance(self, current: Node, neighbor: Node) -> int:
        raise NotImplementedError()

    @abstractmethod
    def heuristic(self, node: Node) -> int:
        raise NotImplementedError()

    def reconstruct_path(
        self,
        current: Node,
        parents: dict[NodeId, Node],
    ) -> list[Node]:
        path = [current]
        current_id = self.identity(current)
        while current_id in parents:
            current = parents[current_id]
            current_id = self.identity(current)
            path.append(current)
        path.reverse()
        return path

    def bfs(self) -> list[Node]:
        visited: set[NodeId] = set()
        frontier: deque[Node] = deque([self.initial()])
        parents: dict[NodeId, Node] = {}

        while frontier:
            current = frontier.popleft()
            if self.goal(current):
                return self.reconstruct_path(current, parents)

            for neighbor in self.neighbors(current):
                neighbor_id = self.identity(neighbor)
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    parents[neighbor_id] = current
                    frontier.append(neighbor)

        raise PathNotFound()

    def dfs(self) -> list[Node]:
        visited: set[NodeId] = set()
        frontier: list[Node] = [self.initial()]
        parents: dict[NodeId, Node] = {}

        while frontier:
            current = frontier.pop()
            if self.goal(current):
                return self.reconstruct_path(current, parents)

            for neighbor in self.neighbors(current):
                neighbor_id = self.identity(neighbor)
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    parents[neighbor_id] = current
                    frontier.append(neighbor)

        raise PathNotFound()

    def astar(self) -> list[Node]:
        initial = self.initial()
        initial_id = self.identity(initial)

        g_score: dict[NodeId, float] = defaultdict(lambda: math.inf)
        g_score[initial_id] = 0

        f_score: dict[NodeId, float] = defaultdict(lambda: math.inf)
        f_score[initial_id] = self.heuristic(initial)

        open_set_ids: set[NodeId] = set([initial_id])
        open_set: list[tuple[int, Node]] = [(0, initial)]
        parents: dict[NodeId, Node] = {}

        while open_set:
            _, current = heapq.heappop(open_set)
            current_id = self.identity(current)
            open_set_ids.remove(current_id)

            if self.goal(current):
                return self.reconstruct_path(current, parents)

            for neighbor in self.neighbors(current):
                neighbor_id = self.identity(neighbor)
                tentative_g_score = g_score[current_id] + self.distance(
                    current, neighbor
                )
                if tentative_g_score < g_score[neighbor_id]:
                    parents[neighbor_id] = current
                    g_score[neighbor_id] = tentative_g_score
                    f = tentative_g_score + self.heuristic(neighbor)
                    f_score[neighbor_id] = f

                    if neighbor_id not in open_set_ids:
                        open_set_ids.add(neighbor_id)
                        heapq.heappush(open_set, (f, neighbor))  # type: ignore

        raise PathNotFound()


class DjikstraMixin:
    def heuristic(self, node: Node) -> int:
        return 0

    def djikstra(self) -> list[Node]:
        return self.astar()
