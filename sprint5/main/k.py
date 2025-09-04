from __future__ import annotations

import os
from collections.abc import Iterable

LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'

if LOCAL:
    class Node:
        def __init__(self, left: Node | None = None, right: Node | None = None, value: int = 0) -> None:
            self.right = right
            self.left = left
            self.value = value


def print_range(node: Node, l: int, r: int) -> None:
    bst = BST(node)
    values_iter = bst.get_range(left=l, right=r)
    print(*values_iter)


class BST:
    root: Node

    def __init__(self, root: Node) -> None:
        self.root = root

    def get_range(self, *, left: int, right: int) -> Iterable[int]:
        return self._get_range(self.root, left=left, right=right)

    def _get_range(self, node: Node | None, *, left: int, right: int) -> Iterable[int]:
        if node is None:
            return

        if left <= node.value <= right:
            yield from self._get_range(node.left, left=left, right=right)
            yield node.value
            yield from self._get_range(node.right, left=left, right=right)
            return

        if node.value < left:
            yield from self._get_range(node.right, left=left, right=right)
        else:
            yield from self._get_range(node.left, left=left, right=right)


def test() -> None:
    node1 = Node(None, None, 2)
    node2 = Node(None, node1, 1)
    node3 = Node(None, None, 8)
    node4 = Node(None, node3, 8)
    node5 = Node(node4, None, 9)
    node6 = Node(node5, None, 10)
    node7 = Node(node2, node6, 5)
    print_range(node7, 2, 8)
    # expected output: 2 5 8 8


if __name__ == '__main__':
    test()
