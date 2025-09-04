from __future__ import annotations

import os

LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'

if LOCAL:
    class Node:
        def __init__(self, value: int, left: Node | None = None, right: Node | None = None) -> None:
            self.value = value
            self.right = right
            self.left = left


def solution(root: Node) -> int:
    return get_height(root)


def get_height(node: Node | None) -> int:
    if node is None:
        return 0

    left_height = get_height(node.left)
    right_height = get_height(node.right)
    result = max(left_height, right_height) + 1

    return result


def test() -> None:
    node1 = Node(1, None, None)
    node2 = Node(4, None, None)
    node3 = Node(3, node1, node2)
    node4 = Node(8, None, None)
    node5 = Node(5, node3, node4)

    assert solution(node5) == 3


if __name__ == '__main__':
    test()
