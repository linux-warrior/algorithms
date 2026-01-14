from __future__ import annotations

import itertools
import sys
from collections.abc import Sequence


def find_longest_common_subsequence(a: Sequence[int], b: Sequence[int]) -> tuple[Sequence[int], Sequence[int]]:
    a_len = len(a)
    b_len = len(b)
    subsequence_lengths = [[0] * (b_len + 1) for _i in range(a_len + 1)]

    for i in range(a_len):
        for j in range(b_len):
            subsequence_lengths[i + 1][j + 1] = (
                subsequence_lengths[i][j] + 1
                if a[i] == b[j] else
                max(subsequence_lengths[i + 1][j], subsequence_lengths[i][j + 1])
            )

    result_len = subsequence_lengths[-1][-1]
    a_result: list[int] = [-1] * result_len
    b_result: list[int] = [-1] * result_len

    result_pos = result_len - 1
    i = a_len - 1
    j = b_len - 1

    while result_pos >= 0:
        if a[i] == b[j]:
            a_result[result_pos] = i
            b_result[result_pos] = j
            result_pos -= 1
            i -= 1
            j -= 1
        elif subsequence_lengths[i][j + 1] == subsequence_lengths[i + 1][j + 1]:
            i -= 1
        else:
            j -= 1

    return a_result, b_result


def main() -> None:
    a_len = int(input().strip())
    a = list(itertools.islice(
        map(int, sys.stdin.readline().split()),
        a_len,
    ))

    b_len = int(input().strip())
    b = list(itertools.islice(
        map(int, sys.stdin.readline().split()),
        b_len,
    ))

    a_subsequence, b_subsequence = find_longest_common_subsequence(a, b)
    print(len(a_subsequence))

    if not a_subsequence:
        return

    for subsequence in (a_subsequence, b_subsequence):
        print(*map(lambda i: i + 1, subsequence))


if __name__ == '__main__':
    main()
