from __future__ import annotations

from collections.abc import MutableSequence


def sift_down(heap: MutableSequence[int], idx: int) -> int:
    heap_obj = Heap(heap)
    return heap_obj.sift_down(idx)


class Heap:
    nodes: MutableSequence[int]

    def __init__(self, nodes: MutableSequence[int]) -> None:
        self.nodes = nodes

    def sift_down(self, index: int) -> int:
        last_node_index = len(self.nodes) - 1

        while True:
            left_child_index = index * 2

            if left_child_index > last_node_index:
                return index

            right_child_index = left_child_index + 1
            largest_child_index: int

            if (
                    right_child_index <= last_node_index and
                    self.nodes[right_child_index] > self.nodes[left_child_index]
            ):
                largest_child_index = right_child_index
            else:
                largest_child_index = left_child_index

            if self.nodes[index] >= self.nodes[largest_child_index]:
                return index

            (
                self.nodes[index],
                self.nodes[largest_child_index],
            ) = (
                self.nodes[largest_child_index],
                self.nodes[index],
            )
            index = largest_child_index


def test() -> None:
    sample = [-1, 12, 1, 8, 3, 4, 7]
    assert sift_down(sample, 2) == 5


if __name__ == '__main__':
    test()
