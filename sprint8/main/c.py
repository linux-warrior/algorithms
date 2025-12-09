from __future__ import annotations

import sys
from collections import Counter
from collections.abc import Iterable


def build_longest_palindrome(line: str) -> Iterable[str]:
    chars_counter = Counter[str](line)
    chars_list = list(chars_counter)
    chars_list.sort()

    middle_char: str | None = None

    for char in chars_list:
        char_count = chars_counter[char]
        char_count_half = char_count >> 1

        if char_count_half:
            yield char * char_count_half

        if char_count & 1 and middle_char is None:
            middle_char = char

    if middle_char is not None:
        yield middle_char

    for char in reversed(chars_list):
        char_count = chars_counter[char]
        char_count_half = char_count >> 1

        if char_count_half:
            yield char * char_count_half


def main() -> None:
    line = sys.stdin.readline().strip()

    print(*build_longest_palindrome(line), sep='')


if __name__ == '__main__':
    main()
