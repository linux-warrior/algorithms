from __future__ import annotations

import os

LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'

if LOCAL:
    class Node:
        def __init__(self, value: str, next_item: Node | None = None) -> None:
            self.value = value
            self.next_item = next_item


def solution(node: Node) -> None:
    current_node: Node | None = node

    while current_node is not None:
        print(current_node.value)
        current_node = current_node.next_item


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
