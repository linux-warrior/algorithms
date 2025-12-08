from __future__ import annotations

import sys
from collections.abc import Iterable


def reverse_word_order(line: str) -> Iterable[str]:
    word_end = len(line)

    while word_end > 0:
        word_boundary = line.rfind(' ', 0, word_end)

        if word_boundary < word_end - 1:
            yield line[word_boundary + 1:word_end]

        word_end = word_boundary


def main() -> None:
    line = sys.stdin.readline().strip()

    print(*reverse_word_order(line))


if __name__ == '__main__':
    main()
