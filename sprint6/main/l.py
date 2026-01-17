from __future__ import annotations

import itertools
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

    def get_unique_neighbors(self) -> Iterable[int]:
        neighbors_set = set[int]()

        for neighbor in self.vertices:
            if neighbor in neighbors_set:
                continue

            neighbors_set.add(neighbor)
            yield neighbor


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

    def is_complete(self) -> bool:
        vertices_count = len(self)

        for vertex, adjacency_list in enumerate(self):
            unique_neighbors = set(adjacency_list.get_unique_neighbors())
            unique_neighbors.discard(vertex)

            if len(unique_neighbors) < vertices_count - 1:
                return False

        return True

    @classmethod
    def read(cls, *, vertices_count: int, edges_count: int, is_directed: bool = True) -> Self:
        graph = cls(vertices_count=vertices_count, is_directed=is_directed)

        for edge in Edge.read_list(edges_count):
            graph.add_edge(edge)

        return graph


def main() -> None:
    vertices_count, edges_count = map(int, input().split())
    graph = Graph.read(
        vertices_count=vertices_count,
        edges_count=edges_count,
        is_directed=False,
    )

    print('YES' if graph.is_complete() else 'NO')


if __name__ == '__main__':
    main()
