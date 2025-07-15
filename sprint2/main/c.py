from __future__ import annotations

import os

LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'

if LOCAL:
    class Node:
        def __init__(self, value: str, next_item: Node | None = None) -> None:
            self.value = value
            self.next_item = next_item


def solution(node: Node, idx: int) -> Node | None:
    current_node: Node | None = node
    previous_node: Node | None = None
    i = 0

    while current_node is not None:
        if i == idx:
            if previous_node is None:
                return current_node.next_item
            else:
                previous_node.next_item = current_node.next_item

        previous_node = current_node
        current_node = current_node.next_item
        i += 1

    return node


def test() -> None:
    node3 = Node('node3', None)
    node2 = Node('node2', node3)
    node1 = Node('node1', node2)
    node0 = Node('node0', node1)
    new_head = solution(node0, 1)

    assert new_head is node0
    assert new_head.next_item is node2
    assert new_head.next_item.next_item is node3
    assert new_head.next_item.next_item.next_item is None

    # result is node0 -> node2 -> node3


if __name__ == '__main__':
    test()
