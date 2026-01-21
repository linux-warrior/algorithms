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

    def is_valid_element(self, row: int, column: int) -> bool:
        return (
                0 <= row < self.rows_count and
                0 <= column < self.columns_count
        )

    def get_neighbours(self, row: int, column: int) -> Sequence[int]:
        if not self.is_valid_element(row, column):
            return []

        result: list[int] = []

        if row > 0:
            result.append(self.elements[row - 1][column])

        if row < self.rows_count - 1:
            result.append(self.elements[row + 1][column])

        if column > 0:
            result.append(self.elements[row][column - 1])

        if column < self.columns_count - 1:
            result.append(self.elements[row][column + 1])

        result.sort()

        return result

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
    row = read_int()
    column = read_int()

    neighbours = matrix.get_neighbours(row, column)
    print(*neighbours)


if __name__ == '__main__':
    main()
