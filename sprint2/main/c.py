from __future__ import annotations

import os

LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'

if LOCAL:
    class Node:
        def __init__(self, value: str, next_item: Node | None = None) -> None:
            self.value = value
            self.next_item = next_item


def solution(node: Node, idx: int) -> Node | None:
    return remove_node(node, idx)


def remove_node(node: Node, index: int) -> Node | None:
    linked_list = LinkedList(node)
    linked_list.remove(index)
    return linked_list.get_head()


class LinkedList:
    head: Node | None

    def __init__(self, head: Node | None = None) -> None:
        self.head = head

    def get_head(self) -> Node | None:
        return self.head

    def remove(self, index: int) -> None:
        if index < 0:
            return

        node: Node | None = self.head
        previous_node: Node | None = None
        i = 0

        while i < index and node is not None:
            previous_node = node
            node = node.next_item
            i += 1

        if node is None:
            return

        if previous_node is None:
            self.head = node.next_item
        else:
            previous_node.next_item = node.next_item


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
