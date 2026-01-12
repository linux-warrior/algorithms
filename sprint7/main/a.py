from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable


def get_max_profit(prices: Iterable[int]) -> int:
    prices_iter = iter(prices)

    try:
        previous_price = next(prices_iter)
    except StopIteration:
        return 0

    result = 0

    for price in prices_iter:
        if price > previous_price:
            result += price - previous_price

        previous_price = price

    return result


def main() -> None:
    prices_count = int(input().strip())
    prices = itertools.islice(
        map(int, sys.stdin.readline().split()),
        prices_count,
    )
    print(get_max_profit(prices))


if __name__ == '__main__':
    main()
