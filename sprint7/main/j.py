from __future__ import annotations

import itertools
import sys
from collections.abc import Sequence


def find_longest_increasing_subsequence(values: Sequence[int]) -> Sequence[int]:
    subsequences = [-1]
    predecessors = [-1] * len(values)
    result_len = 0

    for i, value in enumerate(values):
        left = 1
        right = result_len + 1

        while left < right:
            middle = (left + right) >> 1

            if values[subsequences[middle]] < value:
                left = middle + 1
            else:
                right = middle

        new_result_len = left

        if new_result_len > result_len:
            result_len = new_result_len
            subsequences.append(i)
        else:
            subsequences[new_result_len] = i

        predecessors[i] = subsequences[new_result_len - 1]

    result = [-1] * result_len
    i = subsequences[result_len]

    for j in range(result_len - 1, -1, -1):
        result[j] = i
        i = predecessors[i]

    return result


def main() -> None:
    values_count = int(input().strip())
    values = list(itertools.islice(
        map(int, sys.stdin.readline().split()),
        values_count,
    ))

    subsequence = find_longest_increasing_subsequence(values)
    print(len(subsequence))
    print(*map(lambda i: i + 1, subsequence))


if __name__ == '__main__':
    main()
