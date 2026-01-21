from __future__ import annotations

import itertools
from collections import deque
from collections.abc import Iterable, Iterator
from typing import Self


class Edge:
    vertices: tuple[int, int]

    def __init__(self, vertices: Iterable[int]) -> None:
        vertices_list = list(itertools.islice(vertices, 2))
        self.vertices = vertices_list[0], vertices_list[1]

    def __iter__(self) -> Iterator[int]:
        yield from self.vertices

    def __getitem__(self, index: int) -> int:
        return self.vertices[index]

    def __neg__(self) -> Self:
        return self.__class__([self[1], self[0]])

    @classmethod
    def read(cls) -> Self:
        vertices_iter = map(lambda vertex_str: int(vertex_str) - 1, input().split())
        return cls(vertices_iter)

    @classmethod
    def read_list(cls, count: int) -> Iterable[Self]:
        for i in range(count):
            yield cls.read()


class AdjacencyList:
    vertices: list[int]

    def __init__(self) -> None:
        self.vertices = []

    def __len__(self) -> int:
        return len(self.vertices)

    def __iter__(self) -> Iterator[int]:
        yield from self.vertices

    def add_vertex(self, vertex: int) -> None:
        self.vertices.append(vertex)


class Graph:
    is_directed: bool
    adjacency_lists: list[AdjacencyList]

    def __init__(self, *, vertices_count: int = 0, is_directed: bool = True) -> None:
        self.is_directed = is_directed
        self.adjacency_lists = []
        self.create_vertices(vertices_count)

    def __len__(self) -> int:
        return len(self.adjacency_lists)

    def __iter__(self) -> Iterator[AdjacencyList]:
        yield from self.adjacency_lists

    def __getitem__(self, vertex: int) -> AdjacencyList:
        return self.adjacency_lists[vertex]

    def create_vertices(self, count: int) -> None:
        self.adjacency_lists.extend(AdjacencyList() for _i in range(count))

    def add_edge(self, edge: Edge) -> None:
        self._add_edge(edge)

        if not self.is_directed:
            self._add_edge(-edge)

    def _add_edge(self, edge: Edge) -> None:
        adjacency_list = self.adjacency_lists[edge[0]]
        adjacency_list.add_vertex(edge[1])

    def get_max_distance(self, start_vertex: int) -> int | None:
        bfs = BFS(self)
        visitor = GetMaxDistanceVisitor(vertices_count=len(self))
        bfs.run(start_vertex, visitor=visitor)

        return visitor.get_max_distance()

    @classmethod
    def read(cls, *, vertices_count: int, edges_count: int, is_directed: bool = True) -> Self:
        graph = cls(vertices_count=vertices_count, is_directed=is_directed)

        for edge in Edge.read_list(edges_count):
            graph.add_edge(edge)

        return graph


class VerticesState:
    visited: list[bool]

    def __init__(self, *, vertices_count: int = 0) -> None:
        self.visited = [False] * vertices_count

    def is_visited(self, vertex: int) -> bool:
        return self.visited[vertex]

    def visit(self, vertex: int) -> None:
        self.visited[vertex] = True


class VerticesQueue:
    vertices: deque[int]

    def __init__(self) -> None:
        self.vertices = deque()

    def __bool__(self) -> bool:
        return bool(self.vertices)

    def put(self, vertex: int) -> None:
        self.vertices.append(vertex)

    def get(self) -> int:
        return self.vertices.popleft()


class BFS:
    graph: Graph
    state: VerticesState
    queue: VerticesQueue

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.state = VerticesState()
        self.queue = VerticesQueue()

    def run(self, start_vertex: int, *, visitor: BFSVisitor) -> None:
        self.state = VerticesState(vertices_count=len(self.graph))
        self.queue = VerticesQueue()

        self._visit_vertex(start_vertex, visitor=visitor)

        while self.queue:
            vertex = self.queue.get()

            for neighbor in self.graph[vertex]:
                if not self.state.is_visited(neighbor):
                    self._visit_vertex(neighbor, visitor=visitor, previous_vertex=vertex)

    def _visit_vertex(self, vertex: int, *, previous_vertex: int | None = None, visitor: BFSVisitor) -> None:
        visitor.handle_vertex(vertex, previous_vertex=previous_vertex)
        self.state.visit(vertex)
        self.queue.put(vertex)


class BFSVisitor:
    def handle_vertex(self, vertex: int, *, previous_vertex: int | None = None) -> None:
        pass


class GetMaxDistanceVisitor(BFSVisitor):
    distances: list[int | None]

    def __init__(self, *, vertices_count: int) -> None:
        self.distances = [None] * vertices_count

    def get_max_distance(self) -> int | None:
        return max((distance for distance in self.distances if distance is not None), default=None)

    def handle_vertex(self, vertex: int, *, previous_vertex: int | None = None) -> None:
        self.distances[vertex] = self._get_current_distance(previous_vertex=previous_vertex)

    def _get_current_distance(self, *, previous_vertex: int | None = None) -> int | None:
        if previous_vertex is None:
            return 0

        previous_distance = self.distances[previous_vertex]
        current_distance = previous_distance + 1 if previous_distance is not None else None

        return current_distance


def main() -> None:
    vertices_count, edges_count = map(int, input().split())
    graph = Graph.read(
        vertices_count=vertices_count,
        edges_count=edges_count,
        is_directed=False,
    )
    start_vertex = int(input()) - 1

    max_distance = graph.get_max_distance(start_vertex)
    print(max_distance if max_distance is not None else -1)


if __name__ == '__main__':
    main()
