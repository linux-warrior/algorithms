from __future__ import annotations

import itertools
from collections.abc import Iterable, Iterator
from typing import Self


class Edge:
    vertices: tuple[int, int]

    def __init__(self, *, vertices: Iterable[int]) -> None:
        vertices_list = list(itertools.islice(vertices, 2))
        self.vertices = vertices_list[0], vertices_list[1]

    def __getitem__(self, index: int) -> int:
        return self.vertices[index]

    @classmethod
    def read(cls) -> Self:
        vertices_iter = map(lambda vertex_str: int(vertex_str) - 1, input().split())
        return cls(vertices=vertices_iter)

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

    def as_list(self) -> Iterator[int]:
        yield from map(lambda vertex: vertex + 1, self)

    def add_vertex(self, vertex: int) -> None:
        self.vertices.append(vertex)

    def sort(self) -> None:
        self.vertices.sort()


class Graph:
    adjacency_lists: list[AdjacencyList]

    def __init__(self, *, vertices_count: int = 0) -> None:
        self.adjacency_lists = []
        self.create_vertices(vertices_count)

    def __iter__(self) -> Iterator[AdjacencyList]:
        yield from self.adjacency_lists

    def create_vertices(self, count: int) -> None:
        for i in range(count):
            self.adjacency_lists.append(AdjacencyList())

    def add_edge(self, edge: Edge) -> None:
        adjacency_list = self.adjacency_lists[edge[0]]
        adjacency_list.add_vertex(edge[1])

    def sort(self) -> None:
        for adjacency_list in self:
            adjacency_list.sort()

    @classmethod
    def read(cls, *, vertices_count: int, edges_count: int) -> Self:
        graph = cls(vertices_count=vertices_count)

        for edge in Edge.read_list(edges_count):
            graph.add_edge(edge)

        graph.sort()

        return graph


def main() -> None:
    vertices_count, edges_count = map(int, input().split())
    graph = Graph.read(vertices_count=vertices_count, edges_count=edges_count)

    for adjacency_list in graph:
        print(len(adjacency_list), *adjacency_list.as_list())


if __name__ == '__main__':
    main()
