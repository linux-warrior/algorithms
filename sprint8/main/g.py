from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable, Sequence


def search_with_shift(values: Sequence[int], pattern: Sequence[int]) -> Iterable[int]:
    values_len = len(values)
    pattern_len = len(pattern)

    for i in range(values_len - pattern_len + 1):
        found = True
        shift = values[i] - pattern[0]

        for j in range(1, pattern_len):
            if values[i + j] != pattern[j] + shift:
                found = False
                break

        if found:
            yield i


def main() -> None:
    values_len = int(input().strip())
    values = list(itertools.islice(
        map(int, sys.stdin.readline().split()),
        values_len,
    ))
    pattern_len = int(input().strip())
    pattern = list(itertools.islice(
        map(int, sys.stdin.readline().split()),
        pattern_len,
    ))

    positions_iter = search_with_shift(values, pattern)
    print(*map(lambda position: position + 1, positions_iter))


if __name__ == '__main__':
    main()
