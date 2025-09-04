from __future__ import annotations

import os
from collections.abc import Iterable
from typing import Self

LOCAL = os.environ.get('REMOTE_JUDGE', 'false') != 'true'

if LOCAL:
    class Node:
        def __init__(self, value: int, left: Node | None = None, right: Node | None = None) -> None:
            self.value = value
            self.right = right
            self.left = left


def solution(root: Node) -> int:
    digit_path_tool = DigitPathTool()
    return digit_path_tool.get_paths_sum(root)


class DigitPath:
    digits: list[int]

    def __init__(self, digits: Iterable[int] | None = None) -> None:
        self.digits = list(digits or [])

    def add_digit(self, digit: int) -> Self:
        return self.__class__(self.digits + [digit])

    def as_int(self) -> int:
        if not self.digits:
            return 0

        return int(''.join(map(str, self.digits)))


class DigitPathTool:
    paths_list: list[DigitPath]

    def __init__(self) -> None:
        self.paths_list = []

    def get_paths_sum(self, node: Node) -> int:
        self.paths_list = []

        self._build_paths_list(node, current_path=DigitPath())
        paths_sum = self._calculate_paths_sum()

        return paths_sum

    def _build_paths_list(self, node: Node, *, current_path: DigitPath) -> None:
        current_path = current_path.add_digit(node.value)
        is_leaf = True

        for child_node in (node.left, node.right):
            if child_node is None:
                continue

            is_leaf = False
            self._build_paths_list(child_node, current_path=current_path)

        if is_leaf:
            self.paths_list.append(current_path)

    def _calculate_paths_sum(self) -> int:
        return sum(digit_path.as_int() for digit_path in self.paths_list)


def test() -> None:
    node1 = Node(2, None, None)
    node2 = Node(1, None, None)
    node3 = Node(3, node1, node2)
    node4 = Node(2, None, None)
    node5 = Node(1, node4, node3)

    assert solution(node5) == 275


if __name__ == '__main__':
    test()
