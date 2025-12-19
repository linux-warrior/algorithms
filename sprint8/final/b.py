from __future__ import annotations

import dataclasses
import sys
from collections.abc import Iterable


def can_word_split(s: str, words: Iterable[str]) -> bool:
    trie = Trie(words=words)
    return trie.can_word_split(s)


@dataclasses.dataclass(kw_only=True, slots=True)
class TrieNode:
    is_word_end: bool = False
    children: dict[str, TrieNode] = dataclasses.field(default_factory=dict)


class Trie:
    root: TrieNode

    __slots = (
        'root',
    )

    def __init__(self, *, words: Iterable[str] | None = None) -> None:
        self.root = TrieNode()

        if words is not None:
            self.add_words(words)

    def add_words(self, words: Iterable[str]) -> None:
        for word in words:
            self.add_word(word)

    def add_word(self, word: str) -> None:
        node = self.root

        for char in word:
            child_node = node.children.get(char)

            if child_node is None:
                node.children[char] = child_node = TrieNode()

            node = child_node

        node.is_word_end = True

    def find_word(self, s: str, start_pos: int = 0) -> Iterable[int]:
        node = self.root
        s_length = len(s)
        pos = start_pos

        while True:
            if node.is_word_end:
                yield pos

            if pos >= s_length:
                break

            char = s[pos]
            child_node = node.children.get(char)

            if child_node is None:
                break

            node = child_node
            pos += 1

    def can_word_split(self, s: str) -> bool:
        s_length = len(s)
        results = [False] * (s_length + 1)
        results[0] = True

        for start_pos in range(s_length):
            if not results[start_pos]:
                continue

            for end_pos in self.find_word(s, start_pos):
                results[end_pos] = True

        return results[s_length]


def read_words(count: int) -> Iterable[str]:
    for i in range(count):
        yield sys.stdin.readline().strip()


def main() -> None:
    s = sys.stdin.readline().strip()
    words_count = int(input().strip())
    words = read_words(words_count)

    print('YES' if can_word_split(s, words) else 'NO')


if __name__ == '__main__':
    main()
