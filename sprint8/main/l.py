from __future__ import annotations

import sys
from collections.abc import Sequence


def calculate_prefix_func_array(s: str) -> Sequence[int]:
    s_length = len(s)
    pi_array = [0] * s_length
    pi_value = 0

    for i in range(1, s_length):
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

    print(*calculate_prefix_func_array(s))


if __name__ == '__main__':
    main()
