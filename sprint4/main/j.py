from __future__ import annotations

import itertools
import sys
from collections.abc import Iterable, Sequence


class SubarrayHashTool:
    array: Sequence[int]
    a: int
    m: int

    _prefix_hashes: Sequence[int]
    _a_powers: Sequence[int]

    def __init__(self, array: Sequence[int], *, a: int, m: int) -> None:
        self.array = array
        self.a = a
        self.m = m

        self._prefix_hashes = self._calculate_prefix_hashes()
        self._a_powers = self._calculate_a_powers()

    def _calculate_prefix_hashes(self) -> Sequence[int]:
        result: list[int] = []

        hash_value = 0
        result.append(hash_value)

        for value in self.array:
            hash_value = (hash_value * self.a + value) % self.m
            result.append(hash_value)

        return result

    def _calculate_a_powers(self) -> Sequence[int]:
        result: list[int] = []

        a_power = 1
        result.append(a_power)

        for i in range(len(self.array)):
            a_power = (a_power * self.a) % self.m
            result.append(a_power)

        return result

    def get_hash(self, start: int, end: int) -> int:
        return (self._prefix_hashes[end] - self._prefix_hashes[start] * self._a_powers[end - start]) % self.m

    def get_hashes(self, *, length: int) -> Iterable[int]:
        if length < 1:
            yield 0
            return

        for start in range(0, len(self.array) - length + 1):
            yield self.get_hash(start, start + length)


class SubarrayHashToolSet:
    hash_tools: Iterable[SubarrayHashTool]

    def __init__(self, hash_tools: Iterable[SubarrayHashTool]) -> None:
        self.hash_tools = hash_tools

    def get_hashes(self, *, length: int) -> Iterable[tuple[int]]:
        return zip(*(hash_tool.get_hashes(length=length) for hash_tool in self.hash_tools))


def get_max_common_subarray_length(a: Sequence[int], b: Sequence[int]) -> int:
    result = 0

    a_hash_tools: list[SubarrayHashTool] = []
    b_hash_tools: list[SubarrayHashTool] = []

    for param_a, param_m in [
        (31, 10 ** 9 + 7),
        (37, 10 ** 9 + 9),
    ]:
        a_hash_tools.append(SubarrayHashTool(a, a=param_a, m=param_m))
        b_hash_tools.append(SubarrayHashTool(b, a=param_a, m=param_m))

    a_hash_tool_set = SubarrayHashToolSet(a_hash_tools)
    b_hash_tool_set = SubarrayHashToolSet(b_hash_tools)

    bottom_length = 0
    top_length = min(len(a), len(b))

    while bottom_length <= top_length:
        middle_length = (bottom_length + top_length) // 2

        a_hashes = set(a_hash_tool_set.get_hashes(length=middle_length))
        hashes_intersect = any(
            b_hash in a_hashes
            for b_hash in b_hash_tool_set.get_hashes(length=middle_length)
        )

        if hashes_intersect:
            result = middle_length
            bottom_length = middle_length + 1
        else:
            top_length = middle_length - 1

    return result


def main() -> None:
    a_len = int(input().strip())
    a = list(itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        a_len,
    ))

    b_len = int(input().strip())
    b = list(itertools.islice(
        map(int, sys.stdin.readline().strip().split()),
        b_len,
    ))

    max_common_subarray_length = get_max_common_subarray_length(a, b)
    print(max_common_subarray_length)


if __name__ == '__main__':
    main()
