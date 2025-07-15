from __future__ import annotations

import os

LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'

if LOCAL:
    class Node:
        def __init__(self, value: str, next_item: Node | None = None) -> None:
            self.value = value
            self.next_item = next_item


def solution(node: Node, elem: str) -> int:
    current_node: Node | None = node
    i = 0

    while current_node is not None:
        if current_node.value == elem:
            return i

        current_node = current_node.next_item
        i += 1

    return -1


def test() -> None:
    node3 = Node('node3', None)
    node2 = Node('node2', node3)
    node1 = Node('node1', node2)
    node0 = Node('node0', node1)

    idx = solution(node0, 'node2')
    assert idx == 2


if __name__ == '__main__':
    test()
