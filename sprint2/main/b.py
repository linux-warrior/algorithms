from __future__ import annotations

import os
from collections.abc import Iterator

LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'

if LOCAL:
    class Node:
        def __init__(self, value: str, next_item: Node | None = None) -> None:
            self.value = value
            self.next_item = next_item


def solution(node: Node) -> None:
    print_linked_list(node)


def print_linked_list(node: Node) -> None:
    linked_list = LinkedList(node)

    for value in linked_list.iter_values():
        print(value)


class LinkedList:
    head: Node

    def __init__(self, head: Node) -> None:
        self.head = head

    def __iter__(self) -> Iterator[Node]:
        node: Node | None = self.head

        while node is not None:
            yield node
            node = node.next_item

    def iter_values(self) -> Iterator[str]:
        for node in self:
            yield node.value


def test() -> None:
    node3 = Node('node3', None)
    node2 = Node('node2', node3)
    node1 = Node('node1', node2)
    node0 = Node('node0', node1)
    solution(node0)

    # Output is:
    # node0
    # node1
    # node2
    # node3


if __name__ == '__main__':
    test()
