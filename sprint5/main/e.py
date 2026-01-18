from __future__ import annotations

import os

LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'

if LOCAL:
    class Node:
        def __init__(self, value: int, left: Node | None = None, right: Node | None = None) -> None:
            self.value = value
            self.right = right
            self.left = left


def solution(root: Node) -> bool:
    return is_bst(root)


def is_bst(node: Node | None, *, min_value: int | None = None, max_value: int | None = None) -> bool:
    if node is None:
        return True

    return (
            (min_value is None or min_value < node.value) and
            (max_value is None or node.value < max_value) and
            is_bst(node.left, min_value=min_value, max_value=node.value) and
            is_bst(node.right, min_value=node.value, max_value=max_value)
    )


def test() -> None:
    node1 = Node(1, None, None)
    node2 = Node(4, None, None)
    node3 = Node(3, node1, node2)
    node4 = Node(8, None, None)
    node5 = Node(5, node3, node4)

    assert solution(node5)
    node2.value = 5
    assert not solution(node5)


if __name__ == '__main__':
    test()
