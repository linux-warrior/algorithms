from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable


def get_max_tie_length(results: Iterable[int]) -> int:
    max_tie_length = 0

    tied_intervals = {0: -1}
    results_diff = 0

    for i, result in enumerate(results):
        results_diff += 1 if result else -1
        tie_start = tied_intervals.get(results_diff)

        if tie_start is None:
            tied_intervals[results_diff] = i
            continue

        tie_length = i - tie_start

        if tie_length > max_tie_length:
            max_tie_length = tie_length

    return max_tie_length


def main() -> None:
    results_count = int(input().strip())
    results = itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        results_count,
    )

    max_tie_length = get_max_tie_length(results)
    print(max_tie_length)


if __name__ == '__main__':
    main()
