# https://contest.yandex.ru/contest/23815/run-report/155579456/
#
# -- Принцип работы --
#
# В данной задаче реализован классический алгоритм быстрой сортировки (quicksort) со схемой разбиения
# Хоара (Hoare partition scheme). Сортируемый массив может содержать элементы произвольного типа, для
# которого определен оператор `<`.
#
# Сначала на каждом шаге сортировки в качестве опорного выбирается элемент, расположенный в центре
# обрабатываемого интервала массива. Для сравнения элементов массива используются два указателя,
# изначально содержащие индексы левого и правого элементов интервала. Если левый указатель ссылается
# на элемент не меньший опорного, а правый указатель — на элемент, не больший опорного, то данные
# элементы массива меняются местами.
#
# После того как все элементы интервала массива будут обработаны, а указатели пересекутся, частично
# отсортированный интервал разбивается на две части по второму указателю. Затем два новых интервала
# аналогичным образом сортируются рекурсивно.
#
# -- Доказательство корректности --
#
# На каждом шаге алгоритма интервал массива частично сортируется и разбивается на две части, каждая
# из которых содержит как минимум один элемент. Таким образом, рекурсивная обработка массива рано
# или поздно будет завершена. Подробный анализ алгоритма можно найти в открытых источниках:
# https://en.wikipedia.org/wiki/Quicksort#Hoare_partition_scheme.
#
# -- Временная сложность --
#
# Временная сложность быстрой сортировки со схемой разбиения Хоара в худшем случае составляет `O(n²)` —
# когда при каждом разбиении интервала массива одна из получившихся частей будет содержать только
# один элемент. В лучшем и среднем случаях временная сложность алгоритма составляет `O(n log n)` —
# т. е., сложность пропорциональна произведению числа элементов массива на потенциальную глубину рекурсии.
#
# -- Пространственная сложность --
#
# Пространственная сложность алгоритма в среднем пропорциональна глубине рекурсии и составляет `O(log n)`,
# поскольку при каждом вызове функции сортировки используется фиксированный набор вспомогательных
# локальных переменных.

from __future__ import annotations

import dataclasses
from collections.abc import Iterable, MutableSequence
from typing import Protocol, Self


class Comparable(Protocol):
    def __lt__(self, other: Self) -> bool: ...


def quicksort[T: Comparable](array: MutableSequence[T]) -> None:
    quicksort_helper = QuicksortHelper[T](array)
    quicksort_helper.sort()


class QuicksortHelper[T: Comparable]:
    array: MutableSequence[T]

    def __init__(self, array: MutableSequence[T]) -> None:
        self.array = array

    def sort(self) -> None:
        self._sort(left=0, right=len(self.array) - 1)

    def _sort(self, *, left: int, right: int) -> None:
        if right <= left:
            return

        pivot = self._get_pivot(left=left, right=right)
        i = left - 1
        j = right + 1

        while True:
            while True:
                i += 1

                if not self.array[i] < pivot:
                    break

            while True:
                j -= 1

                if not pivot < self.array[j]:
                    break

            if i >= j:
                break

            self.array[i], self.array[j] = self.array[j], self.array[i]

        self._sort(left=left, right=j)
        self._sort(left=j + 1, right=right)

    def _get_pivot(self, *, left: int, right: int) -> T:
        return self.array[(left + right) // 2]


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
        fields_list = input().split()[:3]

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

    quicksort(participants)

    for participant in participants:
        print(participant.name)


if __name__ == '__main__':
    main()
