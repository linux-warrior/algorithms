from __future__ import annotations

import re


def get_longest_word(line: str) -> str:
    word_pattern = re.compile(r'\w+')
    position = 0
    result = ''

    while True:
        word_match = word_pattern.search(line, position)

        if word_match is None:
            break

        word = word_match.group()
        position = word_match.end()

        if len(word) > len(result):
            result = word

    return result


def main() -> None:
    line_len = int(input().strip())
    line = input().strip()[:line_len]

    longest_word = get_longest_word(line)
    print(longest_word)
    print(len(longest_word))


if __name__ == '__main__':
    main()
