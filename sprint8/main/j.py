from __future__ import annotations

import sys
from collections.abc import Iterable, Iterator, Sequence


def search_names(names: Iterable[str], queries: Iterable[str]) -> Iterable[str]:
    names_trie = NamesTrie(names)

    for query in queries:
        yield from names_trie.search(query)


class NamesTrieNode:
    names: list[str]
    children: dict[str, NamesTrieNode]

    __slots__ = (
        'names',
        'children',
    )

    def __init__(self) -> None:
        self.names = []
        self.children = {}

    def add_name(self, name: str) -> None:
        self.names.append(name)

    def get_names(self) -> Sequence[str]:
        return self.names

    def __getitem__(self, char: str) -> NamesTrieNode | None:
        return self.children.get(char)

    def __setitem__(self, char: str, child_node: NamesTrieNode) -> None:
        self.children[char] = child_node

    def __iter__(self) -> Iterator[NamesTrieNode]:
        yield from self.children.values()

    def __reversed__(self) -> Iterator[NamesTrieNode]:
        return reversed(self.children.values())

    def iter_subtree(self) -> Iterator[NamesTrieNode]:
        nodes_stack: list[NamesTrieNode] = [self]

        while nodes_stack:
            node = nodes_stack.pop()
            yield node

            for child_node in reversed(node):
                nodes_stack.append(child_node)


class NamesTrie:
    root: NamesTrieNode

    __slots__ = (
        'root',
    )

    def __init__(self, names: Iterable[str] | None = None) -> None:
        self.root = NamesTrieNode()

        if names is not None:
            self.add_names(names)

    def add_names(self, names: Iterable[str]) -> None:
        for name in names:
            self.add_name(name)

    def add_name(self, name: str) -> None:
        node = self.root

        for char in name:
            if not char.isupper():
                continue

            child_node = node[char]

            if child_node is None:
                node[char] = child_node = NamesTrieNode()

            node = child_node

        node.add_name(name)

    def search(self, query: str) -> Iterable[str]:
        results = list(self._search_query(query))
        results.sort()
        return results

    def _search_query(self, query: str) -> Iterable[str]:
        if not query:
            yield from self._search_empty_str()
            return

        node = self.root
        child_node: NamesTrieNode | None = None

        for char in query:
            if not char.isupper():
                continue

            child_node = node[char]

            if child_node is None:
                break

            node = child_node

        if child_node is None:
            yield ''
            return

        for subtree_node in child_node.iter_subtree():
            yield from subtree_node.get_names()

    def _search_empty_str(self) -> Iterable[str]:
        for node in self.root.iter_subtree():
            yield from node.get_names()


def read_strings(count: int) -> Iterable[str]:
    for i in range(count):
        yield sys.stdin.readline().strip()


def main() -> None:
    names_count = int(input().strip())
    names = list(read_strings(names_count))
    queries_count = int(input().strip())
    queries = read_strings(queries_count)

    for result in search_names(names, queries):
        print(result)


if __name__ == '__main__':
    main()
