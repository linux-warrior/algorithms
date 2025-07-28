from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable, Sequence


def bubble_sort_interactive(values: Iterable[int]) -> Iterable[Sequence[int]]:
    values_list = list(values)
    values_list_len = len(values_list)
    unsorted_len = values_list_len

    while True:
        new_unsorted_len = 0

        for i in range(1, unsorted_len):
            if values_list[i - 1] > values_list[i]:
                values_list[i], values_list[i - 1] = values_list[i - 1], values_list[i]
                new_unsorted_len = i

        if new_unsorted_len > 0 or unsorted_len == values_list_len:
            yield values_list

        if new_unsorted_len < 2:
            break

        unsorted_len = new_unsorted_len


def main() -> None:
    values_count = int(input().strip())
    values = list(itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        values_count,
    ))

    for values_list in bubble_sort_interactive(values):
        print(*values_list)


if __name__ == '__main__':
    main()
