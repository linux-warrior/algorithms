# https://contest.yandex.ru/contest/22450/run-report/140237614/

from __future__ import annotations

from collections.abc import Iterable

type GridRow = Iterable[int | None]
type Grid = Iterable[GridRow]


def get_max_score(*,
                  grid: Grid,
                  min_digit: int = 1,
                  max_digit: int = 9,
                  max_keys: int,
                  players_count: int = 2) -> int:
    digits_counter = [0] * (max_digit - min_digit + 1)

    for grid_row in grid:
        for digit in grid_row:
            if digit is not None:
                digits_counter[digit - min_digit] += 1

    total_max_keys = max_keys * players_count
    max_score = sum(
        int(0 < digit_count <= total_max_keys)
        for digit_count in digits_counter
    )

    return max_score


def read_int() -> int:
    return int(input().strip())


def read_grid(*, width: int, height: int) -> Grid:
    for y in range(height):
        yield read_grid_row(width=width)


def read_grid_row(*, width: int) -> GridRow:
    for char in input().strip()[:width]:
        digit: int | None = None

        try:
            digit = int(char)
        except ValueError:
            pass

        yield digit


def main() -> None:
    max_keys = read_int()
    grid = read_grid(width=4, height=4)

    max_score = get_max_score(grid=grid, max_keys=max_keys)
    print(max_score)


if __name__ == '__main__':
    main()
