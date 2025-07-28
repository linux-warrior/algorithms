from __future__ import annotations

import itertools
import sys


def counting_sort(values: list[int], *, min_value: int, max_value: int) -> None:
    if not values or min_value > max_value:
        return

    values_counts: list[int] = [0] * (max_value - min_value + 1)

    for value in values:
        values_counts[value - min_value] += 1

    i = 0
    value = min_value

    for value_count in values_counts:
        for j in range(value_count):
            values[i] = value
            i += 1

        value += 1


def main() -> None:
    values_count = int(input().strip())
    values = list(itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        values_count,
    ))

    counting_sort(values, min_value=0, max_value=2)
    print(*values)


if __name__ == '__main__':
    main()
