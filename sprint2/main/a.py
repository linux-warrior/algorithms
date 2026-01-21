from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable, Sequence
from typing import Self


class Matrix:
    elements: Sequence[Sequence[int]]
    rows_count: int
    columns_count: int

    def __init__(self, elements: Iterable[Iterable[int]]) -> None:
        elements_list: list[list[int]] = []
        self.elements = elements_list

        self.rows_count = 0
        columns_count: int | None = None

        for elements_row in elements:
            elements_list_row: list[int]

            if columns_count is None:
                elements_list_row = list(elements_row)
                columns_count = len(elements_list_row)
            else:
                elements_list_row = list(itertools.islice(elements_row, columns_count))

            elements_list.append(elements_list_row)
            self.rows_count += 1

        self.columns_count = columns_count or 0

    def __str__(self) -> str:
        result: list[str] = []

        for elements_row in self.elements:
            result.append(' '.join(map(str, elements_row)))

        return '\n'.join(result)

    def transpose(self) -> Self:
        elements_list = [[0] * self.rows_count for _column_num in range(self.columns_count)]

        for row_num, elements_row in enumerate(self.elements):
            for column_num, element in enumerate(elements_row):
                elements_list[column_num][row_num] = element

        return self.__class__(elements_list)

    @classmethod
    def read(cls, rows_count: int, columns_count: int) -> Self:
        return cls(cls._read_elements(rows_count, columns_count))

    @classmethod
    def _read_elements(cls, rows_count: int, columns_count: int) -> Iterable[Iterable[int]]:
        for row_num in range(rows_count):
            elements_row = map(int, sys.stdin.readline().split())
            yield itertools.islice(elements_row, columns_count)


def read_int() -> int:
    return int(input().strip())


def main() -> None:
    rows_count = read_int()
    columns_count = read_int()
    matrix = Matrix.read(rows_count, columns_count)

    transposed_matrix = matrix.transpose()
    print(transposed_matrix)


if __name__ == '__main__':
    main()
