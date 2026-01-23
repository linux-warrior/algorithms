from __future__ import annotations

import itertools
import sys
from collections.abc import Sequence


def get_sum(x: Sequence[int], k: int) -> Sequence[int]:
    result: list[int] = []
    i = len(x) - 1
    carry = 0

    while i >= 0 or k > 0:
        if i >= 0:
            x_digit = int(x[i])
            i -= 1
        else:
            x_digit = 0

        if k > 0:
            k_digit = k % 10
            k //= 10
        else:
            k_digit = 0

        sum_part = x_digit + k_digit + carry
        sum_digit = sum_part % 10
        carry = sum_part // 10
        result.append(sum_digit)

    if carry:
        result.append(carry)

    result.reverse()

    return result


def read_int() -> int:
    return int(input().strip())


def read_int_array(length: int) -> Sequence[int]:
    return list(itertools.islice(
        map(int, sys.stdin.readline().split()),
        length,
    ))


def main() -> None:
    x_len = read_int()
    x = read_int_array(x_len)
    k = read_int()

    print(*get_sum(x, k))


if __name__ == '__main__':
    main()
