from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable


def get_min_banknotes_count(price: int, *, denominations: Iterable[int]) -> int:
    denominations_list = list(denominations)
    denominations_list.sort()

    inf_count = price + 1
    banknotes_counts: list[int] = [inf_count] * (price + 1)
    banknotes_counts[0] = 0

    for price_value in range(len(banknotes_counts)):
        for denomination in denominations_list:
            if denomination > price_value:
                break

            banknotes_counts[price_value] = min(
                banknotes_counts[price_value],
                banknotes_counts[price_value - denomination] + 1,
            )

    banknotes_count = banknotes_counts[-1]

    return banknotes_count if banknotes_count < inf_count else -1


def main() -> None:
    price = int(input().strip())
    denominations_count = int(input().strip())
    denominations = itertools.islice(
        map(int, sys.stdin.readline().split()),
        denominations_count,
    )

    banknotes_count = get_min_banknotes_count(price, denominations=denominations)
    print(banknotes_count)


if __name__ == '__main__':
    main()
