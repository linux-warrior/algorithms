# FIXME: часть тестов завершаются с ошибкой "time-limit-exceeded"

from __future__ import annotations

import itertools
import sys
from collections.abc import Sequence


def get_max_common_subarray_length(a: Sequence[int], b: Sequence[int]) -> int:
    result = 0
    common_subarray_lengths = [0] * len(b)

    for a_i in range(len(a) - 1, -1, -1):
        previous_length = 0

        for b_i in range(len(b) - 1, -1, -1):
            current_length = common_subarray_lengths[b_i]

            if a[a_i] == b[b_i]:
                common_subarray_lengths[b_i] = previous_length + 1
                result = max(result, common_subarray_lengths[b_i])
            else:
                common_subarray_lengths[b_i] = 0

            previous_length = current_length

    return result


def main() -> None:
    a_len = int(input().strip())
    a = list(itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        a_len,
    ))

    b_len = int(input().strip())
    b = list(itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        b_len,
    ))

    max_common_subarray_length = get_max_common_subarray_length(a, b)
    print(max_common_subarray_length)


if __name__ == '__main__':
    main()
