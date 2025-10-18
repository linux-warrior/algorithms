from __future__ import annotations

import os

LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'

if LOCAL:
    class Node:
        def __init__(self, left: Node | None = None, right: Node | None = None, value: int = 0) -> None:
            self.right = right
            self.left = left
            self.value = value
else:
    from node import Node  # type: ignore[import-not-found,no-redef]


def remove(root: Node, key: int) -> Node | None:
    bst = BST(root)
    bst.remove(key)
    return bst.get_root()


class BST:
    root: Node | None

    def __init__(self, root: Node | None = None) -> None:
        self.root = root

    def get_root(self) -> Node | None:
        return self.root

    def remove(self, key: int) -> None:
        node = self.root
        parent: Node | None = None

        while node is not None and node.value != key:
            parent = node
            node = node.left if key < node.value else node.right

        if node is None:
            return

        if node.left is None or node.right is None:
            self._move_subtree(node, parent=parent)
            return

        self._move_successor(node, parent=parent)

    def _move_subtree(self, node: Node, *, parent: Node | None = None) -> None:
        subtree = node.left if node.left is not None else node.right
        self._replace_node(node, parent=parent, replacement=subtree)

    def _replace_node(self, node: Node, *, parent: Node | None = None, replacement: Node | None = None) -> None:
        if parent is None:
            self.root = replacement
            return

        if node is parent.left:
            parent.left = replacement
        else:
            parent.right = replacement

    def _move_successor(self, node: Node, *, parent: Node | None = None) -> None:
        if node.right is None:
            return

        successor = node.right
        successor_parent = node

        while successor.left is not None:
            successor_parent = successor
            successor = successor.left

        successor.left = node.left

        if successor_parent is not node:
            successor_parent.left = successor.right
            successor.right = node.right

        self._replace_node(node, parent=parent, replacement=successor)


def test() -> None:
    node1 = Node(None, None, 2)
    node2 = Node(node1, None, 3)
    node3 = Node(None, node2, 1)
    node4 = Node(None, None, 6)
    node5 = Node(node4, None, 8)
    node6 = Node(node5, None, 10)
    node7 = Node(node3, node6, 5)

    new_head = remove(node7, 10)

    assert new_head is not None
    assert new_head.value == 5
    assert new_head.right is node5
    assert new_head.right.value == 8


if __name__ == '__main__':
    test()
