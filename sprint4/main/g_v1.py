# FIXME: часть тестов завершаются с ошибкой "time-limit-exceeded"

from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable

type FourTuple = tuple[int, int, int, int]


def find_four_tuples(values: Iterable[int], *, sum_value: int) -> Iterable[FourTuple]:
    values_list = list(values)
    values_list.sort()
    values_list_len = len(values_list)

    previous_a: int | None = None

    for a_i in range(values_list_len - 3):
        a = values_list[a_i]

        if a == previous_a:
            continue

        previous_a = a
        expected_sum_of_three = sum_value - a

        previous_b: int | None = None

        for b_i in range(a_i + 1, values_list_len - 2):
            b = values_list[b_i]

            if b == previous_b:
                continue

            previous_b = b
            expected_sum_of_two = expected_sum_of_three - b

            c_i = b_i + 1
            d_i = values_list_len - 1

            while c_i < d_i:
                c = values_list[c_i]
                d = values_list[d_i]
                sum_of_two = c + d

                if sum_of_two == expected_sum_of_two:
                    yield a, b, c, d
                    break

                if sum_of_two < expected_sum_of_two:
                    c_i += 1
                else:
                    d_i -= 1


def main() -> None:
    values_count = int(input().strip())
    sum_value = int(input().strip())
    values = list(itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        values_count,
    ))

    four_tuples = list(find_four_tuples(values, sum_value=sum_value))
    print(len(four_tuples))

    for four_tuple in four_tuples:
        print(*four_tuple)


if __name__ == '__main__':
    main()
