from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable, Sequence


def find_nth_smallest_diff(values: Iterable[int], *, rank: int) -> int:
    values_list = list(values)

    if not values_list:
        return 0

    values_list.sort()

    diff_min = 0
    diff_max = values_list[-1] - values_list[0]

    while diff_min < diff_max:
        diff_avg = (diff_min + diff_max) // 2
        diff_rank = calculate_diff_rank(values_list, diff=diff_avg)

        if diff_rank >= rank:
            diff_max = diff_avg
        else:
            diff_min = diff_avg + 1

    return diff_min


def calculate_diff_rank(values: Sequence[int], *, diff: int) -> int:
    result = 0

    i = 0
    i_max = len(values) - 1
    j = 1
    j_max = len(values)

    while i < i_max:
        while j < j_max:
            if values[j] - values[i] > diff:
                break

            j += 1

        i += 1
        result += j - i

    return result


def main() -> None:
    values_count = int(input().strip())
    values = list(itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        values_count,
    ))
    rank = int(input().strip())

    diff = find_nth_smallest_diff(values, rank=rank)
    print(diff)


if __name__ == '__main__':
    main()
