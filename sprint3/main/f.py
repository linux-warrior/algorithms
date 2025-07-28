from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable


def get_max_triangle_perimeter(segments_lengths: Iterable[int]) -> int:
    segments_lengths_list = list(segments_lengths)
    segments_lengths_list.sort(reverse=True)

    for c_i in range(len(segments_lengths_list) - 2):
        a = segments_lengths_list[c_i + 1]
        b = segments_lengths_list[c_i + 2]
        c = segments_lengths_list[c_i]

        if c < a + b:
            return a + b + c

    return 0


def main() -> None:
    segments_count = int(input().strip())
    segments_lengths = itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        segments_count,
    )

    max_triangle_perimeter = get_max_triangle_perimeter(segments_lengths)
    print(max_triangle_perimeter)


if __name__ == '__main__':
    main()
