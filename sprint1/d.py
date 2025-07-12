from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable


def get_weather_randomness(temperatures: Iterable[int]) -> int:
    temperatures_iter = iter(temperatures)

    try:
        previous_temperature = next(temperatures_iter)
    except StopIteration:
        return 0

    try:
        current_temperature = next(temperatures_iter)
    except StopIteration:
        return 1

    result = 0

    if previous_temperature > current_temperature:
        result += 1

    for next_temperature in temperatures:
        if current_temperature > max(previous_temperature, next_temperature):
            result += 1

        previous_temperature = current_temperature
        current_temperature = next_temperature

    if current_temperature > previous_temperature:
        result += 1

    return result


def main() -> None:
    temperatures_count = int(input().strip())
    temperatures = itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        temperatures_count,
    )
    print(get_weather_randomness(temperatures))


if __name__ == '__main__':
    main()
