from __future__ import annotations

from collections.abc import Sequence


def merge_sort(array: list[int], left: int, right: int) -> None:
    if right - left <= 1:
        return

    middle = (left + right) // 2
    merge_sort(array, left, middle)
    merge_sort(array, middle, right)

    merged_array = merge(array, left, middle, right)
    i = left

    for elem in merged_array:
        array[i] = elem
        i += 1


def merge(array: Sequence[int], left: int, middle: int, right: int) -> Sequence[int]:
    result = [0] * (right - left)

    i = left
    j = middle
    k = 0

    while i < middle and j < right:
        array_i = array[i]
        array_j = array[j]
        elem: int

        if array_i <= array_j:
            elem = array_i
            i += 1
        else:
            elem = array_j
            j += 1

        result[k] = elem
        k += 1

    while i < middle:
        result[k] = array[i]
        i += 1
        k += 1

    while j < right:
        result[k] = array[j]
        j += 1
        k += 1

    return result


def test() -> None:
    a = [1, 4, 9, 2, 10, 11]
    b = merge(a, 0, 3, 6)
    expected = [1, 2, 4, 9, 10, 11]
    assert b == expected

    c = [1, 4, 2, 10, 1, 2]
    merge_sort(c, 0, 6)
    expected = [1, 1, 2, 2, 4, 10]
    assert c == expected


if __name__ == '__main__':
    test()
