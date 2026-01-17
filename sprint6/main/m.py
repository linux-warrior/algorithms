from __future__ import annotations

import enum
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

    def is_bipartite(self) -> bool:
        bipartite_checker = BipartiteChecker(self)
        return bipartite_checker.check()

    @classmethod
    def read(cls, *, vertices_count: int, edges_count: int, is_directed: bool = True) -> Self:
        graph = cls(vertices_count=vertices_count, is_directed=is_directed)

        for edge in Edge.read_list(edges_count):
            graph.add_edge(edge)

        return graph


class VertexColor(enum.Enum):
    WHITE = 0
    BLUE = 1
    RED = 2

    @classmethod
    def get_first(cls) -> VertexColor:
        return cls.BLUE

    def get_next(self) -> VertexColor:
        if self is self.WHITE:
            return self.get_first()

        return VertexColor.RED if self is VertexColor.BLUE else VertexColor.BLUE


class VerticesState:
    colors: list[VertexColor]

    def __init__(self, *, vertices_count: int = 0) -> None:
        self.colors = [VertexColor.WHITE] * vertices_count

    def is_visited(self, vertex: int) -> bool:
        return self.colors[vertex] is not VertexColor.WHITE

    def visit(self, vertex: int, *, previous_vertex: int | None = None) -> None:
        self.colors[vertex] = (
            VertexColor.get_first()
            if previous_vertex is None
            else self.colors[previous_vertex].get_next()
        )

    def same_partition(self, first_vertex: int, second_vertex: int) -> bool:
        if not (self.is_visited(first_vertex) and self.is_visited(second_vertex)):
            return False

        return self.colors[first_vertex] is self.colors[second_vertex]


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


class BipartiteChecker:
    graph: Graph
    state: VerticesState
    queue: VerticesQueue

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.state = VerticesState()
        self.queue = VerticesQueue()

    def check(self) -> bool:
        vertices_count = len(self.graph)
        self.state = VerticesState(vertices_count=vertices_count)
        self.queue = VerticesQueue()

        for start_vertex in range(vertices_count):
            if self.state.is_visited(start_vertex):
                continue

            if not self._check_component(start_vertex):
                return False

        return True

    def _check_component(self, start_vertex: int) -> bool:
        self._visit_vertex(start_vertex)

        while self.queue:
            vertex = self.queue.get()

            for neighbor in self.graph[vertex]:
                if not self.state.is_visited(neighbor):
                    self._visit_vertex(neighbor, previous_vertex=vertex)

                elif self.state.same_partition(vertex, neighbor):
                    return False

        return True

    def _visit_vertex(self, vertex: int, *, previous_vertex: int | None = None) -> None:
        self.state.visit(vertex, previous_vertex=previous_vertex)
        self.queue.put(vertex)


def main() -> None:
    vertices_count, edges_count = map(int, input().split())
    graph = Graph.read(
        vertices_count=vertices_count,
        edges_count=edges_count,
        is_directed=False,
    )

    print('YES' if graph.is_bipartite() else 'NO')


if __name__ == '__main__':
    main()
