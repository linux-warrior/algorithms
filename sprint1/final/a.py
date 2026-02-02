# https://contest.yandex.ru/contest/22450/run-report/156221955/

from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable


def get_distances_to_zero(numbers: Iterable[str]) -> Iterable[int]:
    zeros_positions: list[int] = []
    i = -1

    for i, number_str in enumerate(numbers):
        if number_str == '0':
            zeros_positions.append(i)

    zeros_count = len(zeros_positions)

    if not zeros_count:
        return

    numbers_count = i + 1
    zero_pos = zeros_positions[0]
    next_zero = 1
    previous_zero_pos: int | None = None

    for i in range(numbers_count):
        if i != zero_pos:
            distance = abs(i - zero_pos)

            if previous_zero_pos is not None:
                distance = min(distance, i - previous_zero_pos)

            yield distance
            continue

        yield 0

        if next_zero < zeros_count:
            previous_zero_pos = zero_pos
            zero_pos = zeros_positions[next_zero]
            next_zero += 1
        else:
            previous_zero_pos = None


def main() -> None:
    numbers_count = int(input().strip())
    numbers = itertools.islice(
        sys.stdin.readline().split(),
        numbers_count,
    )

    distances_iter = get_distances_to_zero(numbers)
    print(*distances_iter)


if __name__ == '__main__':
    main()
