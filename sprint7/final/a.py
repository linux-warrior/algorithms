from __future__ import annotations

import sys


def get_levenstein_distance(a: str, b: str) -> int:
    a_length = len(a)
    b_length = len(b)

    if b_length > a_length:
        return get_levenstein_distance(b, a)

    distances = [0] * (b_length + 1)

    for b_i in range(1, b_length + 1):
        distances[b_i] = b_i

    for a_i in range(1, a_length + 1):
        distances_top_left = distances[0]
        distances[0] = a_i

        for b_i in range(1, b_length + 1):
            distances_top = distances[b_i]
            distances[b_i] = distances_top_left if a[a_i - 1] == b[b_i - 1] else min(
                distances[b_i - 1],
                distances_top_left,
                distances_top,
            ) + 1
            distances_top_left = distances_top

    return distances[b_length]


def main() -> None:
    a = sys.stdin.readline().strip()
    b = sys.stdin.readline().strip()

    print(get_levenstein_distance(a, b))


if __name__ == '__main__':
    main()
