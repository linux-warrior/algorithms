from __future__ import annotations

import abc
import itertools
from collections import defaultdict
from collections.abc import Iterable


class AbstractHash(abc.ABC):
    @abc.abstractmethod
    def get_hash(self, string: str) -> int: ...


class PolynomialHash(AbstractHash):
    a: int
    m: int

    def __init__(self, *, a: int, m: int) -> None:
        self.a = a
        self.m = m

    def get_hash(self, string: str) -> int:
        result = 0

        for char in string:
            result = (result * self.a + ord(char)) % self.m

        return result


class StringsGenerator:
    alphabet: str

    def __init__(self, *, alphabet: str) -> None:
        self.alphabet = alphabet

    def generate(self) -> Iterable[str]:
        length = 0

        while True:
            for chars_tuple in itertools.product(self.alphabet, repeat=length):
                yield ''.join(chars_tuple)

            length += 1


class CollisionsFinder:
    hash_algo: AbstractHash
    strings_iter: Iterable[str]

    def __init__(self,
                 *,
                 hash_algo: AbstractHash,
                 strings_iter: Iterable[str]) -> None:
        self.hash_algo = hash_algo
        self.strings_iter = strings_iter

    def find(self) -> Iterable[tuple[str, str]]:
        previous_strings_dict = defaultdict[int, list[str]](list)

        for string in self.strings_iter:
            hash_value = self.hash_algo.get_hash(string)
            previous_strings_list = previous_strings_dict[hash_value]

            if previous_strings_list:
                yield previous_strings_list[-1], string

            previous_strings_list.append(string)


def main() -> None:
    a = int(input().strip())
    m = int(input().strip())

    hash_algo = PolynomialHash(a=a, m=m)
    strings_generator = StringsGenerator(
        alphabet=''.join(chr(code) for code in range(ord('a'), ord('z') + 1)),
    )
    collisions_finder = CollisionsFinder(
        hash_algo=hash_algo,
        strings_iter=strings_generator.generate(),
    )

    for first_str, second_str in collisions_finder.find():
        print(first_str, second_str)
        break


if __name__ == '__main__':
    main()
