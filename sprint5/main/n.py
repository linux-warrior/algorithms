from __future__ import annotations

import os
from typing import Self

LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'

if LOCAL:
    class Node:
        def __init__(self,
                     left: Node | None = None,
                     right: Node | None = None,
                     value: int = 0,
                     size: int = 0) -> None:
            self.right = right
            self.left = left
            self.value = value
            self.size = size


def split(root: Node, k: int) -> tuple[Node | None, Node | None]:
    bst = BST(root)
    other_bst = bst.split(k)

    return bst.get_root(), other_bst.get_root()


class BST:
    root: Node | None

    def __init__(self, root: Node | None = None) -> None:
        self.root = root

    def get_root(self) -> Node | None:
        return self.root

    def split(self, k: int) -> Self:
        left_part, right_part = self._split_node(self.root, k)
        self.root = left_part

        return self.__class__(right_part)

    def _split_node(self, node: Node | None, k: int) -> tuple[Node | None, Node | None]:
        if node is None:
            return None, None

        elif k <= 0:
            return None, node

        elif k >= node.size:
            return node, None

        left_child = node.left
        left_child_size = left_child.size if left_child else 0

        if k == left_child_size:
            node.left = None
            node.size -= left_child_size

            return left_child, node

        right_child = node.right
        right_child_size = right_child.size if right_child else 0

        if k == left_child_size + 1:
            node.right = None
            node.size -= right_child_size

            return node, right_child

        elif k < left_child_size:
            left_part, right_part = self._split_node(left_child, k)
            node.left = right_part
            right_part_size = right_part.size if right_part else 0
            node.size += right_part_size - left_child_size

            return left_part, node

        else:
            left_part, right_part = self._split_node(right_child, k - left_child_size - 1)
            node.right = left_part
            left_part_size = left_part.size if left_part else 0
            node.size += left_part_size - right_child_size

            return node, right_part


def test() -> None:
    node1 = Node(None, None, 3, 1)
    node2 = Node(None, node1, 2, 2)
    node3 = Node(None, None, 8, 1)
    node4 = Node(None, None, 11, 1)
    node5 = Node(node3, node4, 10, 3)
    node6 = Node(node2, node5, 5, 6)

    left, right = split(node6, 4)
    assert left is not None
    assert right is not None
    assert left.size == 4
    assert right.size == 2


if __name__ == '__main__':
    test()
