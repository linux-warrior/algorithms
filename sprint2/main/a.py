from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable, Sequence


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
            elements_list_row = list(elements_row)

            if columns_count is None:
                columns_count = len(elements_list_row)

            elements_list.append(elements_list_row[:columns_count])
            self.rows_count += 1

        self.columns_count = columns_count or 0

    @classmethod
    def read(cls, rows_count: int, columns_count: int) -> Matrix:
        return cls(cls._read_elements(rows_count, columns_count))

    @classmethod
    def _read_elements(cls, rows_count: int, columns_count: int) -> Iterable[Iterable[int]]:
        for row in range(rows_count):
            elements_row = map(int, sys.stdin.readline().strip().split())
            yield itertools.islice(elements_row, columns_count)

    def __str__(self) -> str:
        result: list[str] = []

        for elements_row in self.elements:
            result.append(' '.join(map(str, elements_row)))

        return '\n'.join(result)

    def transpose(self) -> Matrix:
        elements_list: list[list[int]] = []

        for i in range(self.columns_count):
            elements_list.append([0] * self.rows_count)

        for row_num, elements_row in enumerate(self.elements):
            for column_num, element in enumerate(elements_row):
                elements_list[column_num][row_num] = element

        return Matrix(elements_list)


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
