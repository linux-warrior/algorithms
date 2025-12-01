from __future__ import annotations

import itertools
import sys
from collections.abc import Collection


def can_split_equally(values: Collection[int]) -> bool:
    values_sum = sum(values)

    if values_sum % 2:
        return False

    target_sum = values_sum // 2
    results = [False] * (target_sum + 1)
    results[0] = True

    for value in values:
        for possible_sum in range(target_sum, value - 1, -1):
            if results[possible_sum - value]:
                results[possible_sum] = True

    return results[target_sum]


def main() -> None:
    values_count = int(input().strip())
    values = list(itertools.islice(
        map(int, sys.stdin.readline().split()),
        values_count,
    ))
    print(can_split_equally(values))


if __name__ == '__main__':
    main()
