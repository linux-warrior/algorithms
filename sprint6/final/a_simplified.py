# https://contest.yandex.ru/contest/25070/run-report/148994478/
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
# реализации алгоритма Прима, выбранного в методе `MaxSpanningTreeTool.get_weight()`. Для этого мы
# просуммируем среднее время выполнения наиболее ресурсоемких операций.
#
# * Временная сложность создания массива посещенных вершин, которое выполняется в начале работы функции,
#   составляет `O(|V|)`.
# * Поскольку каждая вершина графа может быть добавлена в очередь конечных вершин ребер не более
#   одного раза, то средний размер очереди составляет `O(|V|)`. Так как мы используем очередь с
#   приоритетом на основе бинарной кучи, то время извлечения из нее элемента составляет `O(log |V|)`.
#   Таким образом, суммарное время извлечения из очереди всех вершин и весов, которые были в нее
#   добавлены, составляет `O(|V| log |V|)`.
# * Поскольку граф неориентированный, то общее количество итераций цикла обработки списков смежности
#   составляет `O(2|E|) = O(|E|)`. Время добавления элемента в очередь конечных вершин составляет
#   `O(log |V|)`. Таким образом, суммарное время добавления в очередь всех обрабатываемых вершин
#   составляет `O(|E| log |V|).
#
# Исходя из вышеизложенного, итоговая вычислительная сложность алгоритма построения MaxST составляет
# `O(|V|) + O(|V| log |V|) + O(|E| log |V|) = O((|V| + |E|) log |V|)`. Если граф связный, то
# `|E| ⩾ |V| - 1`, и поэтому временную сложность алгоритма можно записать в виде `O(|E| log |V|)`.
#
# -- Пространственная сложность --
#
# Пространственная сложность алгоритма в среднем составляет `O(|V| + |E|)`, поскольку во время его
# работы создаются массив посещенных вершин и очередь обрабатываемых ребер.

from __future__ import annotations

import heapq
from collections.abc import Iterable, Iterator
from typing import Self

type Edge = tuple[int, int, int]


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
    adjacency_lists: list[AdjacencyList]

    def __init__(self, *, vertices_count: int = 0) -> None:
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
        self._add_edge((edge[1], edge[0], edge[2]))

    def _add_edge(self, edge: Edge) -> None:
        adjacency_list = self.adjacency_lists[edge[0]]
        adjacency_list.add_vertex(edge[1], weight=edge[2])

    def get_max_spanning_tree_weight(self) -> int | None:
        mst_tool = MaxSpanningTreeTool(self)
        return mst_tool.get_weight()

    @classmethod
    def read(cls, *, vertices_count: int, edges_count: int) -> Self:
        graph = cls(vertices_count=vertices_count)

        for edge in cls._read_edges_list(edges_count):
            graph.add_edge(edge)

        return graph

    @classmethod
    def _read_edges_list(cls, count: int) -> Iterable[Edge]:
        for i in range(count):
            yield cls._read_edge()

    @classmethod
    def _read_edge(cls) -> Edge:
        values_list = list(map(int, input().split()[:3]))
        vertices = list(map(lambda vertex: vertex - 1, values_list[:2]))
        weight = values_list[2]

        return vertices[0], vertices[1], weight


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


class VerticesQueue:
    items: list[tuple[int, int]]

    def __init__(self) -> None:
        self.items = []

    def __bool__(self) -> bool:
        return bool(self.items)

    def put(self, vertex: int, *, weight: int) -> None:
        heapq.heappush(self.items, (-weight, vertex))

    def get(self) -> tuple[int, int]:
        neg_weight, vertex = heapq.heappop(self.items)

        return vertex, -neg_weight


class MaxSpanningTreeTool:
    graph: Graph
    state: VerticesState
    queue: VerticesQueue

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.state = VerticesState()
        self.queue = VerticesQueue()

    def get_weight(self) -> int | None:
        self.state = VerticesState(vertices_count=len(self.graph))
        self.queue = VerticesQueue()
        weight = 0

        self.queue.put(0, weight=0)

        while self.queue:
            vertex, vertex_weight = self.queue.get()

            if self.state.is_visited(vertex):
                continue

            self.state.visit(vertex)
            weight += vertex_weight

            for neighbor, neighbor_weight in self.graph[vertex]:
                if self.state.is_visited(neighbor):
                    continue

                self.queue.put(neighbor, weight=neighbor_weight)

        if self.state.all_visited():
            return weight

        return None


def main() -> None:
    vertices_count, edges_count = map(int, input().split())
    graph = Graph.read(
        vertices_count=vertices_count,
        edges_count=edges_count,
    )

    weight = graph.get_max_spanning_tree_weight()
    print(weight if weight is not None else 'Oops! I did it again')


if __name__ == '__main__':
    main()
