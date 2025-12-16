from __future__ import annotations

import sys
from collections.abc import Iterable, Sequence


def replace(s: str, pattern: str, replacement: str) -> Iterable[str]:
    s_len = len(s)
    pattern_len = len(pattern)

    if s_len == 0 or pattern_len == 0 or s_len < pattern_len:
        yield s
        return

    pi_array = _calculate_prefix_func(pattern)
    i = j = s_pos = 0

    while i < s_len:
        if s[i] != pattern[j]:
            if j == 0:
                i += 1
            else:
                j = pi_array[j - 1]

            continue

        i += 1
        j += 1

        if j < pattern_len:
            continue

        s_part = s[s_pos:i - pattern_len]

        if s_part:
            yield s_part

        if replacement:
            yield replacement

        s_pos = i
        j = 0

    s_part = s[s_pos:]

    if s_part:
        yield s_part


def _calculate_prefix_func(s: str) -> Sequence[int]:
    s_len = len(s)
    pi_array = [0] * s_len
    pi_value = 0

    for i in range(1, s_len):
        current_char = s[i]

        while True:
            previous_char = s[pi_value]
            chars_match = current_char == previous_char

            if chars_match or pi_value == 0:
                break

            pi_value = pi_array[pi_value - 1]

        if chars_match:
            pi_value += 1

        pi_array[i] = pi_value

    return pi_array


def main() -> None:
    s = sys.stdin.readline().strip()
    pattern = sys.stdin.readline().strip()
    replacement = sys.stdin.readline().strip()

    print(*replace(s, pattern, replacement), sep='')


if __name__ == '__main__':
    main()
