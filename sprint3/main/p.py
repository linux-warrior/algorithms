from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable


def get_blocks_count(values: Iterable[int]) -> int:
    result = 0
    values_sum = i_sum = 0

    for i, value in enumerate(values):
        values_sum += value
        i_sum += i

        if values_sum == i_sum:
            result += 1

    return result


def main() -> None:
    values_count = int(input().strip())
    values = list(itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        values_count,
    ))

    blocks_count = get_blocks_count(values)
    print(blocks_count)


if __name__ == '__main__':
    main()
