from __future__ import annotations

import dataclasses
import enum
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

    def __reversed__(self) -> Iterator[int]:
        return reversed(self.vertices)

    def add_vertex(self, vertex: int) -> None:
        self.vertices.append(vertex)

    def sort(self) -> None:
        self.vertices.sort()


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

    def sort(self) -> None:
        for adjacency_list in self:
            adjacency_list.sort()

    def get_vertices_times(self, start_vertex: int) -> Iterable[VertexTime]:
        dfs = DFS(self)
        visitor = GetVerticesTimesVisitor(vertices_count=len(self))
        dfs.run(start_vertex, visitor=visitor)

        return visitor.get_vertices_times()

    @classmethod
    def read(cls, *, vertices_count: int, edges_count: int, is_directed: bool = True) -> Self:
        graph = cls(vertices_count=vertices_count, is_directed=is_directed)

        for edge in Edge.read_list(edges_count):
            graph.add_edge(edge)

        graph.sort()

        return graph


class VertexColor(enum.Enum):
    WHITE = 0
    GRAY = 1
    BLACK = 2


class VerticesState:
    colors: list[VertexColor]

    def __init__(self, *, vertices_count: int = 0) -> None:
        self.colors = [VertexColor.WHITE] * vertices_count

    def is_visited(self, vertex: int) -> bool:
        return self.colors[vertex] is not VertexColor.WHITE

    def is_processed(self, vertex: int) -> bool:
        return self.colors[vertex] is VertexColor.BLACK

    def visit(self, vertex: int) -> None:
        self.colors[vertex] = VertexColor.GRAY

    def process(self, vertex: int) -> None:
        self.colors[vertex] = VertexColor.BLACK


class VerticesStack:
    vertices: list[int]

    def __init__(self) -> None:
        self.vertices = []

    def __bool__(self) -> bool:
        return bool(self.vertices)

    def push(self, vertex: int) -> None:
        self.vertices.append(vertex)

    def pop(self) -> int:
        return self.vertices.pop()


class DFS:
    graph: Graph
    state: VerticesState
    stack: VerticesStack

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.state = VerticesState()
        self.stack = VerticesStack()

    def run(self, start_vertex: int, *, visitor: DFSVisitor) -> None:
        self.state = VerticesState(vertices_count=len(self.graph))
        self.stack = VerticesStack()
        self.stack.push(start_vertex)

        while self.stack:
            vertex = self.stack.pop()

            if not self.state.is_visited(vertex):
                self._visit_vertex(vertex, visitor=visitor)

            elif not self.state.is_processed(vertex):
                self._process_vertex(vertex, visitor=visitor)

    def _visit_vertex(self, vertex: int, *, visitor: DFSVisitor) -> None:
        visitor.start_handle_vertex(vertex)
        self.state.visit(vertex)
        self.stack.push(vertex)

        for neighbor in reversed(self.graph[vertex]):
            if not self.state.is_visited(neighbor):
                self.stack.push(neighbor)

    def _process_vertex(self, vertex: int, *, visitor: DFSVisitor) -> None:
        self.state.process(vertex)
        visitor.end_handle_vertex(vertex)


class DFSVisitor:
    def start_handle_vertex(self, vertex: int) -> None:
        pass

    def end_handle_vertex(self, vertex: int) -> None:
        pass


@dataclasses.dataclass(kw_only=True)
class VertexTime:
    arrival: int | None = None
    departure: int | None = None


class GetVerticesTimesVisitor(DFSVisitor):
    arrival_times: list[int | None]
    departure_times: list[int | None]
    current_time: int

    def __init__(self, *, vertices_count: int) -> None:
        self.arrival_times = [None] * vertices_count
        self.departure_times = [None] * vertices_count
        self.current_time = 0

    def get_vertices_times(self) -> Iterable[VertexTime]:
        for arrival_time, departure_time in zip(self.arrival_times, self.departure_times):
            yield VertexTime(arrival=arrival_time, departure=departure_time)

    def start_handle_vertex(self, vertex: int) -> None:
        self.arrival_times[vertex] = self.current_time
        self.current_time += 1

    def end_handle_vertex(self, vertex: int) -> None:
        self.departure_times[vertex] = self.current_time
        self.current_time += 1


def main() -> None:
    vertices_count, edges_count = map(int, input().split())
    graph = Graph.read(
        vertices_count=vertices_count,
        edges_count=edges_count,
    )

    vertices_times = graph.get_vertices_times(0)

    for vertex_time in vertices_times:
        print(vertex_time.arrival, vertex_time.departure)


if __name__ == '__main__':
    main()
