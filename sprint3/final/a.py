from __future__ import annotations

from collections.abc import Sequence


def broken_search(nums: Sequence[int], target: int) -> int:
    left = 0
    right = len(nums) - 1

    while left <= right:
        middle = (left + right) // 2

        if nums[middle] == target:
            return middle

        if any([
            nums[left] <= target < nums[middle],
            nums[left] > nums[middle] and not nums[middle] < target <= nums[right],
        ]):
            right = middle - 1
        else:
            left = middle + 1

    return -1


def test() -> None:
    arr = [19, 21, 100, 101, 1, 4, 5, 7, 12]
    assert broken_search(arr, 5) == 6


if __name__ == '__main__':
    test()
