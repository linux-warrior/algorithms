from __future__ import annotations

import itertools
import sys
from collections import defaultdict
from collections.abc import Iterable, Sequence


def group_anagrams(words: Iterable[str]) -> Iterable[Sequence[int]]:
    word_indices_dict = defaultdict[str, list[int]](list)

    for i, word in enumerate(words):
        word_indices_dict[''.join(sorted(word))].append(i)

    return word_indices_dict.values()


def main() -> None:
    words_count = int(input().strip())
    words = list(itertools.islice(
        sys.stdin.readline().strip().split(),
        words_count,
    ))

    for word_indices_list in group_anagrams(words):
        print(*word_indices_list)


if __name__ == '__main__':
    main()
