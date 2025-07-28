from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable


def get_satisfied_children_count(*, greed_factors: Iterable[int], cookies_sizes: Iterable[int]) -> int:
    greed_factors_list = list(greed_factors)

    if not greed_factors_list:
        return 0

    cookies_sizes_list = list(cookies_sizes)

    if not cookies_sizes_list:
        return 0

    greed_factors_list.sort()
    cookies_sizes_list.sort()

    i = j = 0

    while True:
        if greed_factors_list[i] <= cookies_sizes_list[j]:
            i += 1

            if i == len(greed_factors_list):
                break

        j += 1

        if j == len(cookies_sizes_list):
            break

    return i


def main() -> None:
    children_count = int(input().strip())
    greed_factors = itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        children_count,
    )

    cookies_count = int(input().strip())
    cookies_sizes = itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        cookies_count,
    )

    satisfied_children_count = get_satisfied_children_count(
        greed_factors=greed_factors,
        cookies_sizes=cookies_sizes,
    )
    print(satisfied_children_count)


if __name__ == '__main__':
    main()
