from __future__ import annotations

import sys


def get_shortest_rep_count(s: str) -> int:
    s_length = len(s)

    if s_length == 0:
        return 1

    shortest_rep_length = s_length - _calculate_prefix_func(s)

    if s_length % shortest_rep_length != 0:
        return 1

    return s_length // shortest_rep_length


def _calculate_prefix_func(s: str) -> int:
    s_length = len(s)

    if s_length == 0:
        return 0

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

    return pi_array[-1]


def main() -> None:
    s = sys.stdin.readline().strip()

    print(get_shortest_rep_count(s))


if __name__ == '__main__':
    main()
