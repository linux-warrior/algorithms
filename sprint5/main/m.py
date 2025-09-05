from __future__ import annotations

from collections.abc import MutableSequence


def sift_up(heap: MutableSequence[int], idx: int) -> int:
    heap_obj = Heap(heap)
    return heap_obj.sift_up(idx)


class Heap:
    nodes: MutableSequence[int]

    def __init__(self, nodes: MutableSequence[int]) -> None:
        self.nodes = nodes

    def sift_up(self, index: int) -> int:
        while True:
            if index == 1:
                return index

            parent_index = index // 2

            if self.nodes[index] <= self.nodes[parent_index]:
                return index

            (
                self.nodes[index],
                self.nodes[parent_index],
            ) = (
                self.nodes[parent_index],
                self.nodes[index],
            )
            index = parent_index


def test() -> None:
    sample = [-1, 12, 6, 8, 3, 15, 7]
    assert sift_up(sample, 5) == 1


if __name__ == '__main__':
    test()
