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
    return get_max_value(root)


def get_max_value(node: Node) -> int:
    candidates: list[int] = [node.value]

    if node.left is not None:
        candidates.append(solution(node.left))

    if node.right is not None:
        candidates.append(solution(node.right))

    return max(candidates)


def test() -> None:
    node1 = Node(1)
    node2 = Node(-5)
    node3 = Node(3, node1, node2)
    node4 = Node(2, node3, None)
    assert solution(node4) == 3


if __name__ == '__main__':
    test()
