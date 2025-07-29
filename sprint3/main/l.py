from __future__ import annotations

import bisect
import itertools
import sys
from collections.abc import Sequence


def find_day_of_purchase(*, savings_timeline: Sequence[int], price: int) -> int:
    day_of_purchase = bisect.bisect_left(savings_timeline, price)

    if day_of_purchase == len(savings_timeline):
        return -1

    return day_of_purchase + 1


def main() -> None:
    savings_timeline_length = int(input().strip())
    savings_timeline = list(itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        savings_timeline_length,
    ))
    price = int(input().strip())

    day_of_purchase_1 = find_day_of_purchase(savings_timeline=savings_timeline, price=price)
    day_of_purchase_2 = find_day_of_purchase(savings_timeline=savings_timeline, price=price * 2)
    print(day_of_purchase_1, day_of_purchase_2)


if __name__ == '__main__':
    main()
