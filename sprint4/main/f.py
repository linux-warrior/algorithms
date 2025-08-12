from __future__ import annotations

import sys
from collections.abc import Iterable, Sequence


class SubstringHashTool:
    string: str
    a: int
    m: int

    _prefix_hashes: Sequence[int]
    _a_powers: Sequence[int]

    def __init__(self, string: str, *, a: int, m: int) -> None:
        self.string = string
        self.a = a
        self.m = m

        self._prefix_hashes = self._calculate_prefix_hashes()
        self._a_powers = self._calculate_a_powers()

    def _calculate_prefix_hashes(self) -> Sequence[int]:
        result = []

        hash_value = 0
        result.append(hash_value)

        for char in self.string:
            hash_value = (hash_value * self.a + ord(char)) % self.m
            result.append(hash_value)

        return result

    def _calculate_a_powers(self) -> Sequence[int]:
        result = []

        a_power = 1
        result.append(a_power)

        for i in range(len(self.string)):
            a_power = (a_power * self.a) % self.m
            result.append(a_power)

        return result

    def get_hash(self, start: int, end: int) -> int:
        return (self._prefix_hashes[end] - self._prefix_hashes[start] * self._a_powers[end - start]) % self.m


def read_slices(count: int) -> Iterable[tuple[int, int]]:
    for i in range(count):
        start, end = map(int, input().strip().split())
        yield start - 1, end


def main() -> None:
    a = int(input().strip())
    m = int(input().strip())
    string = sys.stdin.readline().strip()
    slices_count = int(input().strip())
    slices_iter = read_slices(slices_count)

    substring_hash_tool = SubstringHashTool(string, a=a, m=m)

    for start, end in slices_iter:
        hash_value = substring_hash_tool.get_hash(start, end)
        print(hash_value)


if __name__ == '__main__':
    main()
