# https://contest.yandex.ru/contest/24810/run-report/146445411/
#
# -- Принцип работы --
#
# В данной задаче реализован алгоритм пирамидальной сортировки (heapsort) по возрастанию (неубыванию).
# Сортируемый массив может содержать элементы произвольного типа, для которого определен оператор `<`.
#
# Алгоритм состоит из следующих шагов:
#
# * Создаем пустую неубывающую бинарную кучу (min-heap).
# * По очереди вставляем все элементы массива в кучу, сохраняя ее свойства. Для этого каждый новый
#   элемент кучи мы просеиваем вверх (sift up), пока куча снова не станет упорядоченной.
# * Извлекаем первый элемент из кучи и перемещаем на его место последний элемент. После этого мы
#   восстанавливаем свойства кучи, выполняя просеивание нового первого элемента вниз (sift down).
#   А извлеченный элемент мы добавляем в конец массива, предназначенного для хранения результата
#   сортировки.
# * Повторяем предыдущую операцию до тех пор, пока куча снова не станет пустой.
#
# -- Доказательство корректности --
#
# На третьем шаге описанного выше алгоритма из кучи каждый раз извлекается элемент с минимальным
# значением. Таким образом, на выходе мы получаем массив элементов, отсортированный по возрастанию.
#
# -- Временная сложность --
#
# Временная сложность пирамидальной сортировки в среднем и худшем случаях составляет `O(n log n)`.
# В лучшем случае — когда все элементы массива равны друг другу — временная сложность сортировки
# составляет `O(n)`, поскольку при таких исходных данных просеивание кучи и вниз, и вверх каждый
# раз выполняется за константное время.
#
# -- Пространственная сложность --
#
# Пространственная сложность алгоритма составляет `O(n)`, поскольку во время его работы создается
# куча, в которую добавляются все элементы массива. А затем все элементы кучи поочередно перемещаются
# в отдельный массив, содержащий конечный результат сортировки.

from __future__ import annotations

import dataclasses
from collections.abc import Iterable, Sequence
from typing import Protocol, Self


class Comparable(Protocol):
    def __lt__(self, other: Self) -> bool: ...


def heapsort[T: Comparable](array: Sequence[T]) -> Sequence[T]:
    heap = Heap[T](array)
    result: list[T] = []

    while heap:
        result.append(heap.pop())

    return result


class Heap[T: Comparable]:
    nodes: list[T]

    def __init__(self, nodes: Iterable[T]) -> None:
        self.nodes = []

        for node in nodes:
            self.push(node)

    def __bool__(self) -> bool:
        return bool(self.nodes)

    def push(self, node: T) -> None:
        self.nodes.append(node)
        self._sift_up(len(self.nodes) - 1)

    def _sift_up(self, index: int) -> None:
        while True:
            if index == 0:
                return

            parent_index = (index - 1) // 2

            if not self.nodes[index] < self.nodes[parent_index]:
                return

            (
                self.nodes[index],
                self.nodes[parent_index],
            ) = (
                self.nodes[parent_index],
                self.nodes[index],
            )
            index = parent_index

    def pop(self) -> T:
        if not self.nodes:
            raise ValueError('Heap is empty')

        head = self.nodes[0]
        self.nodes[0] = self.nodes[-1]
        self.nodes.pop()

        if self.nodes:
            self._sift_down(0)

        return head

    def _sift_down(self, index: int) -> None:
        last_node_index = len(self.nodes) - 1

        while True:
            left_child_index = index * 2 + 1

            if left_child_index > last_node_index:
                return

            right_child_index = left_child_index + 1
            smallest_child_index: int

            if (
                    right_child_index <= last_node_index and
                    self.nodes[right_child_index] < self.nodes[left_child_index]
            ):
                smallest_child_index = right_child_index
            else:
                smallest_child_index = left_child_index

            if not self.nodes[smallest_child_index] < self.nodes[index]:
                return

            (
                self.nodes[index],
                self.nodes[smallest_child_index],
            ) = (
                self.nodes[smallest_child_index],
                self.nodes[index],
            )
            index = smallest_child_index


@dataclasses.dataclass(kw_only=True)
class Participant(Comparable):
    name: str
    score: int
    penalty: int

    def __lt__(self, other: Self) -> bool:
        return self.get_comparison_key() < other.get_comparison_key()

    def get_comparison_key(self) -> Comparable:
        return (
            -self.score,
            self.penalty,
            self.name,
        )

    @classmethod
    def read(cls) -> Self:
        fields_list = input().split()

        return cls(
            name=fields_list[0],
            score=int(fields_list[1]),
            penalty=int(fields_list[2]),
        )

    @classmethod
    def read_list(cls, count: int) -> Iterable[Self]:
        for i in range(count):
            yield cls.read()


def main() -> None:
    participants_count = int(input().strip())
    participants = list(Participant.read_list(participants_count))

    participants = list(heapsort(participants))

    for participant in participants:
        print(participant.name)


if __name__ == '__main__':
    main()
