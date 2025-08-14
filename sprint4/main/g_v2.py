# FIXME: часть тестов завершаются с ошибкой "memory-limit-exceeded"

from __future__ import annotations

import itertools
import sys
from collections import defaultdict
from collections.abc import Sequence
from typing import cast

type TwoTuple = tuple[int, int]
type FourTuple = tuple[int, int, int, int]


def find_four_tuples(values: Sequence[int], *, sum_value: int) -> Sequence[FourTuple]:
    four_tuples_set = set[FourTuple]()

    two_tuples_dict = defaultdict[int, set[TwoTuple]](set)
    values_len = len(values)

    for a_i in range(values_len - 1):
        a = values[a_i]

        for b_i in range(a_i + 1, values_len):
            b = values[b_i]
            sum_of_two = a + b
            expected_sum_of_two = sum_value - sum_of_two

            for c_i, d_i in two_tuples_dict[expected_sum_of_two]:
                if len({a_i, b_i, c_i, d_i}) == 4:
                    four_tuples_set.add(cast(
                        FourTuple,
                        tuple(sorted((a, b, values[c_i], values[d_i]))),
                    ))

            two_tuples_dict[sum_of_two].add((a_i, b_i))

    return sorted(four_tuples_set)


def main() -> None:
    values_count = int(input().strip())
    sum_value = int(input().strip())
    values = list(itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        values_count,
    ))

    four_tuples = find_four_tuples(values, sum_value=sum_value)
    print(len(four_tuples))

    for four_tuple in four_tuples:
        print(*four_tuple)


if __name__ == '__main__':
    main()
