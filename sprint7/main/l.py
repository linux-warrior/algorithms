from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable


def get_knapsack_weight(items_weights: Iterable[int], *, capacity: int) -> int:
    knapsack_exists = [False] * (capacity + 1)
    knapsack_exists[0] = True
    result = 0

    for item_weight in items_weights:
        for total_weight in range(capacity, item_weight - 1, -1):
            if not knapsack_exists[total_weight - item_weight]:
                continue

            knapsack_exists[total_weight] = True
            result = max(result, total_weight)

    return result


def main() -> None:
    items_count, capacity = map(int, input().split())
    items_weights = itertools.islice(
        map(int, sys.stdin.readline().split()),
        items_count,
    )

    knapsack_weight = get_knapsack_weight(items_weights, capacity=capacity)
    print(knapsack_weight)


if __name__ == '__main__':
    main()
