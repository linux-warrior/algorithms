from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable


def get_purchased_houses_count(*, houses_prices: Iterable[int], budget: int) -> int:
    houses_prices_list = list(houses_prices)
    houses_prices_list.sort()

    result = 0

    for house_price in houses_prices_list:
        if house_price > budget:
            break

        budget -= house_price
        result += 1

    return result


def main() -> None:
    houses_count, budget = map(int, input().strip().split())
    houses_prices = itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        houses_count,
    )

    purchased_houses_count = get_purchased_houses_count(
        houses_prices=houses_prices,
        budget=budget,
    )
    print(purchased_houses_count)


if __name__ == '__main__':
    main()
