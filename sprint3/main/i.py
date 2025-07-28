from __future__ import annotations

import heapq
import itertools
import sys
from collections import Counter
from collections.abc import Iterable, Sequence


def get_most_common(values: Iterable[int], n: int) -> Sequence[int]:
    counter = Counter[int](values)
    most_common_items = heapq.nlargest(n, counter.items(), key=lambda item: (item[1], -item[0]))
    return [item[0] for item in most_common_items]


def main() -> None:
    values_count = int(input().strip())
    values = list(itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        values_count,
    ))
    most_common_count = int(input().strip())

    most_common_values = get_most_common(values, most_common_count)
    print(*most_common_values)


if __name__ == '__main__':
    main()
