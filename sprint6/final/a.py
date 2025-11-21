# https://contest.yandex.ru/contest/25070/run-report/149551847/
#
# -- Принцип работы --
#
# Методы для создания и дальнейшей работы с графом реализованы в классе `Graph`, причем для представления
# ребер в памяти используются списки смежности. Метод `Graph.get_max_spanning_tree_weight()` возвращает
# суммарный вес ребер, образующих максимальное остовное дерево (MaxST) неориентированного графа.
# Построение MaxST осуществляется с помощью модифицированного алгоритма Прима, в котором для хранения
# очереди весов обрабатываемых ребер и их конечных вершин используется невозрастающая бинарная куча
# (max-heap). Если MaxST построить невозможно (т.е., граф не является связным), то функция возвращает
# `None`.
#
# -- Доказательство корректности --
#
# Доказательство корректности алгоритма Прима можно найти в открытых источниках:
# https://en.wikipedia.org/wiki/Prim's_algorithm#Proof_of_correctness.
#
# -- Временная сложность --
#
# Пусть `|V|` — число вершин графа, а `|E|` — число его ребер. Рассчитаем временную сложность варианта
# реализации алгоритма Прима, выбранного в методе `MaxSpanningTreeTool.run()`. Для этого мы просуммируем
# среднее время выполнения наиболее ресурсоемких операций.
#
# * Временная сложность создания массива посещенных вершин, которое выполняется в начале работы функции,
#   составляет `O(|V|)`.
# * Поскольку граф неориентированный, то число пар конечных вершин ребер и их весов равно `2|E|`, и
#   поэтому средний размер очереди составляет `O(2|E|) = O(|E|)`. Так как мы используем очередь с
#   приоритетом на основе бинарной кучи, то время извлечения из нее элемента составляет `O(log |E|)`.
#   Таким образом, суммарное время извлечения из очереди всех вершин и весов, которые были в нее
#   добавлены, составляет `O(|E| log |E|)`.
# * Поскольку граф неориентированный, то общее количество итераций цикла обработки списков смежности
#   составляет `O(2|E|) = O(|E|)`. Время добавления элемента в очередь конечных вершин составляет
#   `O(log |E|)`. Таким образом, суммарное время добавления в очередь всех обрабатываемых вершин
#   составляет `O(|E| log |E|).
#
# Исходя из вышеизложенного, итоговая вычислительная сложность алгоритма построения MaxST составляет
# `O(|V|) + O(|E| log |E|) + O(|E| log |E|) = O(|V| + |E| log |E|)`. Если граф связный, то
# `|E| ⩾ |V| - 1`, и поэтому временную сложность алгоритма можно записать в виде `O(|E| log |E|)`.
#
# -- Пространственная сложность --
#
# Пространственная сложность алгоритма в среднем составляет `O(|V| + |E|)`, поскольку во время его
# работы создаются массив посещенных вершин и очередь обрабатываемых ребер.

from __future__ import annotations

import heapq
import itertools
from collections.abc import Iterable, Iterator
from typing import Self


class Edge:
    vertices: tuple[int, int]
    weight: int

    __slots__ = ('vertices', 'weight')

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
        values_list = list(map(int, input().split()[:3]))
        vertices = map(lambda vertex: vertex - 1, values_list[:2])
        weight = values_list[2]

        return cls(vertices, weight=weight)

    @classmethod
    def read_list(cls, count: int) -> Iterable[Self]:
        for i in range(count):
            yield cls.read()


type EdgeVertex = tuple[int, int]


class AdjacencyList:
    vertices: list[int]
    weights: list[int]

    __slots__ = ('vertices', 'weights')

    def __init__(self) -> None:
        self.vertices = []
        self.weights = []

    def __len__(self) -> int:
        return len(self.vertices)

    def __iter__(self) -> Iterator[EdgeVertex]:
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
        self.adjacency_lists.extend(AdjacencyList() for _i in range(count))

    def add_edge(self, edge: Edge) -> None:
        self._add_edge(edge)

        if not self.is_directed:
            self._add_edge(-edge)

    def _add_edge(self, edge: Edge) -> None:
        adjacency_list = self.adjacency_lists[edge[0]]
        adjacency_list.add_vertex(edge[1], weight=edge.get_weight())

    def get_max_spanning_tree_weight(self) -> int | None:
        mst_tool = MaxSpanningTreeTool(self)

        try:
            mst_tool.run()
        except MaxSpanningTreeException:
            return None

        return mst_tool.get_weight()

    @classmethod
    def read(cls, *, vertices_count: int, edges_count: int, is_directed: bool = True) -> Self:
        graph = cls(vertices_count=vertices_count, is_directed=is_directed)

        for edge in Edge.read_list(edges_count):
            graph.add_edge(edge)

        return graph


class VerticesState:
    visited: list[bool]
    visited_count: int

    def __init__(self, *, vertices_count: int = 0) -> None:
        self.visited = [False] * vertices_count
        self.visited_count = 0

    def all_visited(self) -> bool:
        return self.visited_count == len(self.visited)

    def is_visited(self, vertex: int) -> bool:
        return self.visited[vertex]

    def visit(self, vertex: int) -> None:
        self.visited[vertex] = True
        self.visited_count += 1


type VerticesQueueItem = tuple[int, int]


class VerticesQueue:
    items: list[VerticesQueueItem]

    def __init__(self) -> None:
        self.items = []

    def __bool__(self) -> bool:
        return bool(self.items)

    def put(self, vertex: int, *, weight: int) -> None:
        heapq.heappush(self.items, (-weight, vertex))

    def get(self) -> EdgeVertex:
        neg_weight, vertex = heapq.heappop(self.items)

        return vertex, -neg_weight


class MaxSpanningTreeException(Exception):
    pass


class DisconnectedGraphException(MaxSpanningTreeException):
    pass


class MaxSpanningTreeTool:
    graph: Graph
    state: VerticesState
    queue: VerticesQueue
    weight: int

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.state = VerticesState()
        self.queue = VerticesQueue()
        self.weight = 0

    def get_weight(self) -> int:
        return self.weight

    def run(self) -> None:
        self.state = VerticesState(vertices_count=len(self.graph))
        self.queue = VerticesQueue()
        self.weight = 0

        self.queue.put(0, weight=0)

        while self.queue:
            vertex, vertex_weight = self.queue.get()

            if self.state.is_visited(vertex):
                continue

            self.state.visit(vertex)
            self.weight += vertex_weight

            for neighbor, neighbor_weight in self.graph[vertex]:
                if self.state.is_visited(neighbor):
                    continue

                self.queue.put(neighbor, weight=neighbor_weight)

        if not self.state.all_visited():
            raise DisconnectedGraphException


def main() -> None:
    vertices_count, edges_count = map(int, input().split())
    graph = Graph.read(
        vertices_count=vertices_count,
        edges_count=edges_count,
        is_directed=False,
    )

    weight = graph.get_max_spanning_tree_weight()
    print(weight if weight is not None else 'Oops! I did it again')


if __name__ == '__main__':
    main()
