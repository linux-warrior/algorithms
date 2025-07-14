from __future__ import annotations

from collections import Counter
from collections.abc import Sequence

type Grid = Sequence[Sequence[int | None]]


def get_max_score(*, grid: Grid, max_keys: int, players_count: int = 2) -> int:
    counter = Counter[int]()

    for grid_row in grid:
        for digit in grid_row:
            if digit is not None:
                counter[digit] += 1

    result = 0
    total_max_keys = max_keys * players_count

    for digit_count in counter.values():
        if digit_count <= total_max_keys:
            result += 1

    return result


def read_int() -> int:
    return int(input().strip())


def read_grid(*, width: int, height: int) -> Grid:
    grid: list[list[int | None]] = []

    for y in range(height):
        grid_row: list[int | None] = []
        grid.append(grid_row)

        for char in input().strip()[:width]:
            digit: int | None

            try:
                digit = int(char)
            except ValueError:
                digit = None

            grid_row.append(digit)

        if len(grid_row) < width:
            grid_row.extend([None] * (width - len(grid_row)))

    return grid


def main() -> None:
    max_keys = read_int()
    grid = read_grid(width=4, height=4)

    max_score = get_max_score(grid=grid, max_keys=max_keys)
    print(max_score)


if __name__ == '__main__':
    main()
