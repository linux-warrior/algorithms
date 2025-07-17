# https://contest.yandex.ru/contest/22450/run-report/140233499/

from __future__ import annotations

import itertools
import sys
from collections.abc import Sequence


def get_distances_to_zero(numbers: Sequence[int]) -> Sequence[int]:
    result: list[int] = []
    distance = -1

    for number in numbers:
        if number == 0:
            distance = 0
        elif distance >= 0:
            distance += 1

        result.append(distance)

    distance = -1

    for i in range(len(numbers) - 1, -1, -1):
        number = numbers[i]

        if number == 0:
            distance = 0
        elif distance >= 0:
            distance += 1
        else:
            continue

        previous_distance = result[i]

        if previous_distance < 0 or distance < previous_distance:
            result[i] = distance

    return result


def main() -> None:
    numbers_count = int(input().strip())
    numbers = list(itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        numbers_count,
    ))

    distances_list = get_distances_to_zero(numbers)
    print(*distances_list)


if __name__ == '__main__':
    main()
