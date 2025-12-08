from __future__ import annotations

import sys


def is_edit_distance_1_or_0(a: str, b: str) -> bool:
    a_length = len(a)
    b_length = len(b)

    if abs(a_length - b_length) > 1:
        return False

    if a_length < b_length:
        return is_edit_distance_1_or_0(b, a)

    distance = 0
    a_i = b_i = 0

    while b_i < b_length:
        if a[a_i] == b[b_i]:
            a_i += 1
            b_i += 1
            continue

        if distance:
            return False

        distance += 1
        a_i += 1

        if a_length == b_length:
            b_i += 1

    if a_i < a_length:
        distance += 1

    return distance <= 1


def main() -> None:
    a = sys.stdin.readline().strip()
    b = sys.stdin.readline().strip()

    print('OK' if is_edit_distance_1_or_0(a, b) else 'FAIL')


if __name__ == '__main__':
    main()
