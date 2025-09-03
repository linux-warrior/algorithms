from __future__ import annotations

import os

LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'

if LOCAL:
    class Node:
        def __init__(self, value: int, left: Node | None = None, right: Node | None = None) -> None:
            self.value = value
            self.right = right
            self.left = left


def solution(root) -> bool:
    return are_symmetrical(root.left, root.right)


def are_symmetrical(first: Node | None, second: Node | None) -> bool:
    if first is None and second is None:
        return True

    if first is None or second is None:
        return False

    return all([
        first.value == second.value,
        are_symmetrical(first.left, second.right),
        are_symmetrical(first.right, second.left),
    ])


def test() -> None:
    node1 = Node(3, None, None)
    node2 = Node(4, None, None)
    node3 = Node(4, None, None)
    node4 = Node(3, None, None)
    node5 = Node(2, node1, node2)
    node6 = Node(2, node3, node4)
    node7 = Node(1, node5, node6)
    assert solution(node7)


if __name__ == '__main__':
    test()
