from __future__ import annotations

import heapq
import itertools
from collections.abc import Iterable, Iterator, Sequence
from typing import Self


class Edge:
    vertices: tuple[int, int]
    weight: int

    def __init__(self, vertices: Iterable[int], *, weight: int) -> None:
        vertices_list = list(itertools.islice(vertices, 2))
        self.vertices = vertices_list[0], vertices_list[1]
        self.weight = weight

    def __iter__(self) -> Iterator[int]:
        yield from self.vertices

    def __getitem__(self, index: int) -> int:
        return self.vertices[index]

    def __neg__(self) -> Self:
        return self.__class__([self[1], self[0]], weight=self.weight)

    def get_weight(self) -> int:
        return self.weight

    @classmethod
    def read(cls) -> Self:
        values_list = list(map(int, input().split()))
        vertices = map(lambda vertex: vertex - 1, values_list[:2])
        weight = values_list[2]

        return cls(vertices, weight=weight)

    @classmethod
    def read_list(cls, count: int) -> Iterable[Self]:
        for i in range(count):
            yield cls.read()


class AdjacencyList:
    vertices: list[int]
    weights: list[int]

    def __init__(self) -> None:
        self.vertices = []
        self.weights = []

    def __len__(self) -> int:
        return len(self.vertices)

    def __iter__(self) -> Iterator[tuple[int, int]]:
        yield from zip(self.vertices, self.weights)

    def add_vertex(self, vertex: int, *, weight: int) -> None:
        self.vertices.append(vertex)
        self.weights.append(weight)


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
        for i in range(count):
            self.adjacency_lists.append(AdjacencyList())

    def add_edge(self, edge: Edge) -> None:
        self._add_edge(edge)

        if not self.is_directed:
            self._add_edge(-edge)

    def _add_edge(self, edge: Edge) -> None:
        adjacency_list = self.adjacency_lists[edge[0]]
        adjacency_list.add_vertex(edge[1], weight=edge.get_weight())

    def get_distances(self, start_vertex: int) -> Sequence[int | None]:
        dijkstra = Dijkstra(self)
        dijkstra.run(start_vertex)

        return dijkstra.get_distances()

    @classmethod
    def read(cls, *, vertices_count: int, edges_count: int, is_directed: bool = True) -> Self:
        graph = cls(vertices_count=vertices_count, is_directed=is_directed)

        for edge in Edge.read_list(edges_count):
            graph.add_edge(edge)

        return graph


class VerticesDistances:
    distances: list[int | None]

    def __init__(self, *, vertices_count: int = 0) -> None:
        self.distances = [None] * vertices_count

    def get_list(self) -> Sequence[int | None]:
        return self.distances

    def update(self, vertex: int, *, distance: int) -> bool:
        current_distance = self.distances[vertex]

        if current_distance is None or current_distance > distance:
            self.distances[vertex] = distance
            return True

        return False


class VerticesQueue:
    items: list[tuple[int, int]]

    def __init__(self) -> None:
        self.items = []

    def __bool__(self) -> bool:
        return bool(self.items)

    def put(self, vertex: int, *, distance: int) -> None:
        heapq.heappush(self.items, (distance, vertex))

    def get(self) -> tuple[int, int]:
        distance, vertex = heapq.heappop(self.items)

        return vertex, distance


class Dijkstra:
    graph: Graph
    distances: VerticesDistances
    queue: VerticesQueue

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.distances = VerticesDistances()
        self.queue = VerticesQueue()

    def get_distances(self) -> Sequence[int | None]:
        return self.distances.get_list()

    def run(self, start_vertex: int) -> None:
        self.distances = VerticesDistances(vertices_count=len(self.graph))
        self.queue = VerticesQueue()

        self._visit_vertex(start_vertex, distance=0)

        while self.queue:
            vertex, vertex_distance = self.queue.get()

            for neighbor, weight in self.graph[vertex]:
                neighbor_distance = vertex_distance + weight
                self._visit_vertex(neighbor, distance=neighbor_distance)

    def _visit_vertex(self, vertex: int, *, distance: int) -> None:
        if self.distances.update(vertex, distance=distance):
            self.queue.put(vertex, distance=distance)


def main() -> None:
    vertices_count, edges_count = map(int, input().split())
    graph = Graph.read(
        vertices_count=vertices_count,
        edges_count=edges_count,
        is_directed=False,
    )

    for start_vertex in range(len(graph)):
        distances = graph.get_distances(start_vertex)
        print(*map(lambda distance: distance if distance is not None else -1, distances))


if __name__ == '__main__':
    main()
