from __future__ import annotations

import itertools
from collections.abc import Iterable, Iterator
from typing import Self


class Edge:
    vertices: tuple[int, int]

    def __init__(self, vertices: Iterable[int]) -> None:
        vertices_list = list(itertools.islice(vertices, 2))
        self.vertices = vertices_list[0], vertices_list[1]

    def __getitem__(self, index: int) -> int:
        return self.vertices[index]

    @classmethod
    def read(cls) -> Self:
        vertices_iter = map(lambda vertex_str: int(vertex_str) - 1, input().split())
        return cls(vertices_iter)

    @classmethod
    def read_list(cls, count: int) -> Iterable[Self]:
        for i in range(count):
            yield cls.read()


class AdjacencyMatrix:
    rows: list[AdjacencyRow]

    def __init__(self, *, vertices_count: int = 0) -> None:
        self.rows = []
        self.create_vertices(vertices_count)

    def __len__(self) -> int:
        return len(self.rows)

    def __iter__(self) -> Iterator[AdjacencyRow]:
        yield from self.rows

    def create_vertices(self, count: int) -> None:
        vertices_count = len(self) + count

        for row in self:
            row.create_vertices(count)

        self.rows.extend(AdjacencyRow(vertices_count=vertices_count) for _i in range(count))

    def add_edge(self, edge: Edge) -> None:
        adjacency_row = self.rows[edge[0]]
        adjacency_row.add_vertex(edge[1])


class AdjacencyRow:
    vertices: list[bool]

    def __init__(self, *, vertices_count: int = 0) -> None:
        self.vertices = []
        self.create_vertices(vertices_count)

    def __iter__(self) -> Iterator[bool]:
        yield from self.vertices

    def as_list(self) -> Iterable[int]:
        return map(int, self)

    def create_vertices(self, count: int) -> None:
        self.vertices.extend([False] * count)

    def add_vertex(self, vertex: int) -> None:
        self.vertices[vertex] = True


class Graph:
    adjacency_matrix: AdjacencyMatrix

    def __init__(self, *, vertices_count: int = 0) -> None:
        self.adjacency_matrix = AdjacencyMatrix(vertices_count=vertices_count)

    def __iter__(self) -> Iterator[AdjacencyRow]:
        yield from self.adjacency_matrix

    def create_vertices(self, count: int) -> None:
        self.adjacency_matrix.create_vertices(count)

    def add_edge(self, edge: Edge) -> None:
        self.adjacency_matrix.add_edge(edge)

    @classmethod
    def read(cls, *, vertices_count: int, edges_count: int) -> Self:
        graph = cls(vertices_count=vertices_count)

        for edge in Edge.read_list(edges_count):
            graph.add_edge(edge)

        return graph


def main() -> None:
    vertices_count, edges_count = map(int, input().split())
    graph = Graph.read(vertices_count=vertices_count, edges_count=edges_count)

    for adjacency_row in graph:
        print(*adjacency_row.as_list())


if __name__ == '__main__':
    main()
