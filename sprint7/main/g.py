from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable


def get_banknotes_combinations_count(amount: int, *, denominations: Iterable[int]) -> int:
    denominations_list = list(denominations)
    denominations_list.sort()

    combinations_counts = [0] * (amount + 1)
    combinations_counts[0] = 1

    for denomination in denominations_list:
        if denomination > amount:
            break

        for amount_value in range(denomination, amount + 1):
            combinations_counts[amount_value] += combinations_counts[amount_value - denomination]

    return combinations_counts[-1]


def main() -> None:
    amount = int(input().strip())
    denominations_count = int(input().strip())
    denominations = itertools.islice(
        map(int, sys.stdin.readline().split()),
        denominations_count,
    )

    combinations_count = get_banknotes_combinations_count(amount, denominations=denominations)
    print(combinations_count)


if __name__ == '__main__':
    main()
