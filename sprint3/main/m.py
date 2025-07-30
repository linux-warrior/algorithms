from __future__ import annotations

import itertools
import math
import sys
from collections.abc import Sequence


def find_median(a: Sequence[int], b: Sequence[int]) -> float:
    a_length = len(a)
    b_length = len(b)

    if a_length > b_length:
        return find_median(b, a)

    a_left = 0
    a_right = a_length
    half_merged_length = (a_length + b_length + 1) // 2

    while a_left <= a_right:
        a_middle = (a_left + a_right) // 2
        b_middle = half_merged_length - a_middle

        a_median_1 = -math.inf if a_middle == 0 else a[a_middle - 1]
        a_median_2 = math.inf if a_middle == a_length else a[a_middle]

        b_median_1 = -math.inf if b_middle == 0 else b[b_middle - 1]
        b_median_2 = math.inf if b_middle == b_length else b[b_middle]

        if a_median_1 > b_median_2:
            a_right = a_middle - 1
            continue

        if b_median_1 > a_median_2:
            a_left = a_middle + 1
            continue

        if (a_length + b_length) % 2 == 0:
            return (max(a_median_1, b_median_1) + min(a_median_2, b_median_2)) / 2
        else:
            return max(a_median_1, b_median_1)

    raise ValueError('Both arrays must be sorted')


def main() -> None:
    a_length = int(input().strip())
    b_length = int(input().strip())

    a = list(itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        a_length,
    ))
    b = list(itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        b_length,
    ))

    median = find_median(a, b)
    print(median if median % 1 else int(median))


if __name__ == '__main__':
    main()
