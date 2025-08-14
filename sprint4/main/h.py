from __future__ import annotations

import sys


def get_max_substr_len(string: str) -> int:
    result = 0

    start_pos = 0
    substr_chars_set = set[str]()

    for end_pos, end_char in enumerate(string):
        while end_char in substr_chars_set:
            substr_chars_set.remove(string[start_pos])
            start_pos += 1

        substr_chars_set.add(string[end_pos])
        result = max(result, end_pos - start_pos + 1)

    return result


def main() -> None:
    string = sys.stdin.readline().strip()

    max_substr_len = get_max_substr_len(string)
    print(max_substr_len)


if __name__ == '__main__':
    main()
