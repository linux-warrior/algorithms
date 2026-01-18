from __future__ import annotations

import os

LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'

if LOCAL:
    class Node:
        def __init__(self, value: int, left: Node | None = None, right: Node | None = None) -> None:
            self.value = value
            self.right = right
            self.left = left


def solution(root1: Node, root2: Node) -> bool:
    return are_equal(root1, root2)


def are_equal(first: Node | None, second: Node | None) -> bool:
    if first is None and second is None:
        return True

    if first is None or second is None:
        return False

    return (
            first.value == second.value and
            are_equal(first.left, second.left) and
            are_equal(first.right, second.right)
    )


def test() -> None:
    node1 = Node(1, None, None)
    node2 = Node(2, None, None)
    node3 = Node(3, node1, node2)

    node4 = Node(1, None, None)
    node5 = Node(2, None, None)
    node6 = Node(3, node4, node5)

    assert solution(node3, node6)


if __name__ == '__main__':
    test()
