from __future__ import annotations

import dataclasses
import os

LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'

if LOCAL:
    class Node:
        def __init__(self, value: int, left: Node | None = None, right: Node | None = None) -> None:
            self.value = value
            self.right = right
            self.left = left


def solution(root: Node) -> bool:
    root_balance = get_node_balance(root)

    return root_balance.is_balanced


@dataclasses.dataclass(kw_only=True)
class NodeBalance:
    is_balanced: bool
    height: int


def get_node_balance(node: Node | None) -> NodeBalance:
    if node is None:
        return NodeBalance(
            is_balanced=True,
            height=0,
        )

    left_balance = get_node_balance(node.left)
    right_balance = get_node_balance(node.right)

    is_balanced = all([
        left_balance.is_balanced,
        right_balance.is_balanced,
        abs(left_balance.height - right_balance.height) <= 1,
    ])
    height = max(left_balance.height, right_balance.height) + 1

    return NodeBalance(
        is_balanced=is_balanced,
        height=height,
    )


def test() -> None:
    node1 = Node(1)
    node2 = Node(-5)
    node3 = Node(3, node1, node2)
    node4 = Node(10)
    node5 = Node(2, node3, node4)
    assert solution(node5)


if __name__ == '__main__':
    test()
