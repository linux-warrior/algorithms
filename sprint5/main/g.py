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
    max_path_sum_tool = MaxPathSumTool()
    return max_path_sum_tool.get_max_sum(root)


class MaxPathSumTool:
    max_sum: int | None

    def __init__(self) -> None:
        self.max_sum = None

    def get_max_sum(self, node: Node) -> int:
        self.max_sum = None
        self._calculate_max_sum(node)

        return self.max_sum or 0

    def _calculate_max_sum(self, node: Node | None) -> int:
        if node is None:
            return 0

        left_max_sum = max(0, self._calculate_max_sum(node.left))
        right_max_sum = max(0, self._calculate_max_sum(node.right))
        current_max_sum = left_max_sum + node.value + right_max_sum

        if self.max_sum is None:
            self.max_sum = current_max_sum
        else:
            self.max_sum = max(self.max_sum, current_max_sum)

        return node.value + max(left_max_sum, right_max_sum)


def test() -> None:
    node1 = Node(5, None, None)
    node2 = Node(1, None, None)
    node3 = Node(-3, node2, node1)
    node4 = Node(2, None, None)
    node5 = Node(2, node4, node3)
    assert solution(node5) == 6


if __name__ == '__main__':
    test()
