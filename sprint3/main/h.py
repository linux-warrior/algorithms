from __future__ import annotations

import functools
import itertools
import locale
import sys
from collections.abc import Iterable, Sequence


def build_largest_number(numbers: Iterable[str]) -> Sequence[str]:
    def compare_combinations(a: str, b: str) -> int:
        return locale.strcoll(a + b, b + a)

    numbers_list = list(numbers)
    numbers_list.sort(key=functools.cmp_to_key(compare_combinations), reverse=True)
    return numbers_list


def main() -> None:
    numbers_count = int(input().strip())
    numbers = itertools.islice(
        sys.stdin.readline().strip().split(),
        numbers_count,
    )

    largest_number = build_largest_number(numbers)
    print(*largest_number, sep='')


if __name__ == '__main__':
    main()
