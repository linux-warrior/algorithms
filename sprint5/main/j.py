from __future__ import annotations

import os

LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'

if not LOCAL:
    from node import Node  # type: ignore[import-not-found]

if LOCAL:
    class Node:  # type: ignore[no-redef]
        def __init__(self, left: Node | None = None, right: Node | None = None, value: int = 0) -> None:
            self.right = right
            self.left = left
            self.value = value


def insert(root: Node, key: int) -> Node:
    bst = BST(root)
    bst.insert(key)

    return root


class BST:
    root: Node

    def __init__(self, root: Node) -> None:
        self.root = root

    def insert(self, key: int) -> None:
        current_node: Node | None = self.root

        while current_node is not None:
            if key < current_node.value:
                if current_node.left is not None:
                    current_node = current_node.left
                    continue

                current_node.left = Node(value=key)
                return

            else:
                if current_node.right is not None:
                    current_node = current_node.right
                    continue

                current_node.right = Node(value=key)
                return


def test() -> None:
    node1 = Node(None, None, 7)
    node2 = Node(node1, None, 8)
    node3 = Node(None, node2, 7)
    new_head = insert(node3, 6)
    assert new_head is node3
    assert new_head.left.value == 6


if __name__ == '__main__':
    test()
