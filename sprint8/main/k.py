from __future__ import annotations

import sys
from collections.abc import Iterable


def compare_even_chars(a: str, b: str) -> int:
    a_chars_iter = iter(_filter_even_chars(a))
    b_chars_iter = iter(_filter_even_chars(b))
    a_char: str | None
    b_char: str | None

    while True:
        try:
            a_char = next(a_chars_iter)
        except StopIteration:
            a_char = None

        try:
            b_char = next(b_chars_iter)
        except StopIteration:
            b_char = None

        if a_char is None and b_char is None:
            return 0

        elif a_char is None:
            return -1

        elif b_char is None:
            return 1

        elif a_char < b_char:
            return -1

        elif a_char > b_char:
            return 1


def _filter_even_chars(s: str) -> Iterable[str]:
    return filter(lambda char: ord(char) & 1 == 0, s)


def main() -> None:
    a = sys.stdin.readline().strip()
    b = sys.stdin.readline().strip()

    print(compare_even_chars(a, b))


if __name__ == '__main__':
    main()
