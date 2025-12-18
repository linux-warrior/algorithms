from __future__ import annotations

import sys
from collections.abc import Iterable, Sequence


def get_max_common_prefix_length(strings: Sequence[str]) -> int:
    strings_count = len(strings)

    if not strings_count:
        return 0

    min_length = min(len(s) for s in strings)
    first_str = strings[0]
    char_i = 0

    while char_i < min_length:
        char = first_str[char_i]

        for str_i in range(1, strings_count):
            if strings[str_i][char_i] != char:
                return char_i

        char_i += 1

    return char_i


def read_strings(count: int) -> Iterable[str]:
    for i in range(count):
        yield sys.stdin.readline().strip()


def main() -> None:
    strings_count = int(input().strip())
    strings = list(read_strings(strings_count))

    print(get_max_common_prefix_length(strings))


if __name__ == '__main__':
    main()
