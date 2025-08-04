from __future__ import annotations

import dataclasses
import locale
from collections.abc import Callable, Iterable, MutableSequence
from typing import Self

type CompareFunc[T] = Callable[[T, T], int]


def quicksort[T](array: MutableSequence[T], *, cmp_func: CompareFunc[T]) -> None:
    quicksort_helper = QuicksortHelper(array, cmp_func=cmp_func)
    quicksort_helper.sort(left=0, right=len(array) - 1)


class QuicksortHelper[T]:
    array: MutableSequence[T]
    cmp_func: CompareFunc[T]

    def __init__(self, array: MutableSequence[T], *, cmp_func: CompareFunc[T]) -> None:
        self.array = array
        self.cmp_func = cmp_func

    def sort(self, *, left: int, right: int) -> None:
        if right <= left:
            return

        pivot = self.array[(left + right) // 2]
        i = left - 1
        j = right + 1

        while True:
            while True:
                i += 1

                if self.cmp_func(self.array[i], pivot) >= 0:
                    break

            while True:
                j -= 1

                if self.cmp_func(self.array[j], pivot) <= 0:
                    break

            if i >= j:
                break

            self.array[i], self.array[j] = self.array[j], self.array[i]

        self.sort(left=left, right=j)
        self.sort(left=j + 1, right=right)


@dataclasses.dataclass(kw_only=True)
class Participant:
    name: str
    score: int
    penalty: int

    def compare(self, other: Participant) -> int:
        if self.score != other.score:
            return self.score - other.score

        if self.penalty != other.penalty:
            return other.penalty - self.penalty

        return locale.strcoll(other.name, self.name)

    @classmethod
    def read(cls) -> Self:
        fields_list = input().strip().split()

        return cls(
            name=fields_list[0],
            score=int(fields_list[1]),
            penalty=int(fields_list[2]),
        )

    @classmethod
    def read_list(cls, count: int) -> Iterable[Self]:
        for i in range(count):
            yield cls.read()


def main() -> None:
    participants_count = int(input().strip())
    participants = list(Participant.read_list(participants_count))

    quicksort(participants, cmp_func=lambda a, b: b.compare(a))

    for participant in participants:
        print(participant.name)


if __name__ == '__main__':
    main()
