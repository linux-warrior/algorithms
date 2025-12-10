from __future__ import annotations

import sys
from collections import Counter
from collections.abc import Iterable


def get_most_frequent_word(words: Iterable[str]) -> str | None:
    words_counter = Counter[str](words)

    if not words_counter:
        return None

    max_frequency = max(words_counter.values())
    result: str | None = None

    for word, frequency in words_counter.items():
        if frequency < max_frequency:
            continue

        if result is None or word < result:
            result = word

    return result


def read_words(count: int) -> Iterable[str]:
    for i in range(count):
        yield sys.stdin.readline().strip()


def main() -> None:
    words_count = int(input().strip())
    words = list(read_words(words_count))

    print(get_most_frequent_word(words))


if __name__ == '__main__':
    main()
