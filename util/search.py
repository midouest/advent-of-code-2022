import math
import heapq
from typing import TypeVar, Callable, Hashable
from collections import deque, defaultdict


Node = TypeVar("Node")
NodeId = TypeVar("NodeId", bound=Hashable)


class PathNotFound(Exception):
    ...


def reconstruct_path(
    current: Node,
    identity_fn: Callable[[Node], NodeId],
    parents: dict[NodeId, Node],
) -> list[Node]:
    path = [current]
    current_id = identity_fn(current)
    while current_id in parents:
        current = parents[current_id]
        current_id = identity_fn(current)
        path.append(current)
    path.reverse()
    return path


def bfs(
    initial: Node,
    identity_fn: Callable[[Node], NodeId],
    neighbor_fn: Callable[[Node], list[Node]],
    goal_fn: Callable[[Node], bool],
) -> list[Node]:
    visited: set[NodeId] = set()
    frontier: deque[Node] = deque([initial])
    parents: dict[NodeId, Node] = {}

    while frontier:
        current = frontier.popleft()
        if goal_fn(current):
            return reconstruct_path(current, identity_fn, parents)

        for neighbor in neighbor_fn(current):
            neighbor_id = identity_fn(neighbor)
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                parents[neighbor_id] = current
                frontier.append(neighbor)

    raise PathNotFound()


def dfs(
    initial: Node,
    identity_fn: Callable[[Node], NodeId],
    neighbor_fn: Callable[[Node], list[Node]],
    goal_fn: Callable[[Node], bool],
) -> list[Node]:
    visited: set[NodeId] = set()
    frontier: list[Node] = [initial]
    parents: dict[NodeId, Node] = {}

    while frontier:
        current = frontier.pop()
        if goal_fn(current):
            return reconstruct_path(current, identity_fn, parents)

        for neighbor in neighbor_fn(current):
            neighbor_id = identity_fn(neighbor)
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                parents[neighbor_id] = current
                frontier.append(neighbor)

    raise PathNotFound()


def astar(
    initial: Node,
    identity_fn: Callable[[Node], NodeId],
    neighbor_fn: Callable[[Node], list[Node]],
    goal_fn: Callable[[Node], bool],
    distance_fn: Callable[[Node, Node], int],
    heuristic_fn: Callable[[Node], int],
) -> list[Node]:
    initial_id = identity_fn(initial)

    g_score: dict[NodeId, float] = defaultdict(lambda: math.inf)
    g_score[initial_id] = 0

    f_score: dict[NodeId, float] = defaultdict(lambda: math.inf)
    f_score[initial_id] = heuristic_fn(initial)

    open_set_ids: set[NodeId] = set([initial_id])
    open_set: list[tuple[int, Node]] = [(0, initial)]
    parents: dict[NodeId, Node] = {}

    while open_set:
        _, current = heapq.heappop(open_set)
        current_id = identity_fn(current)
        open_set_ids.remove(current_id)

        if goal_fn(current):
            return reconstruct_path(current, identity_fn, parents)

        for neighbor in neighbor_fn(current):
            neighbor_id = identity_fn(neighbor)
            tentative_g_score = g_score[current_id] + distance_fn(current, neighbor)
            if tentative_g_score < g_score[neighbor_id]:
                parents[neighbor_id] = current
                g_score[neighbor_id] = tentative_g_score
                f = tentative_g_score + heuristic_fn(neighbor)
                f_score[neighbor_id] = f

                if neighbor_id not in open_set_ids:
                    heapq.heappush(open_set, (f, neighbor))  # type: ignore

    raise PathNotFound()


def djikstra(
    initial: Node,
    identity_fn: Callable[[Node], NodeId],
    neighbor_fn: Callable[[Node], list[Node]],
    goal_fn: Callable[[Node], bool],
    distance_fn: Callable[[Node, Node], int],
) -> list[Node]:
    return astar(
        initial,
        identity_fn,
        neighbor_fn,
        goal_fn,
        distance_fn,
        lambda _: 0,
    )
