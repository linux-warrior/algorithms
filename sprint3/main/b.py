from __future__ import annotations

import dataclasses
from collections.abc import Iterable, Sequence
from typing import ClassVar


@dataclasses.dataclass(kw_only=True)
class LettersCombinationState:
    combination: str = ''
    sequence_pos: int = 0


class LettersCombinationsGenerator:
    letters: ClassVar[Sequence[str]] = [
        '',
        '',
        'abc',
        'def',
        'ghi',
        'jkl',
        'mno',
        'pqrs',
        'tuv',
        'wxyz',
    ]
    sequence: list[int]

    def __init__(self, sequence: Iterable[int]) -> None:
        self.sequence = list(sequence)

    def generate(self) -> Iterable[str]:
        yield from self._generate(state=LettersCombinationState())

    def _generate(self, *, state: LettersCombinationState) -> Iterable[str]:
        if state.sequence_pos == len(self.sequence):
            yield state.combination
            return

        digit = self.sequence[state.sequence_pos]

        if digit < 0 or digit > 9:
            return

        for letter in self.letters[digit]:
            yield from self._generate(state=LettersCombinationState(
                combination=state.combination + letter,
                sequence_pos=state.sequence_pos + 1,
            ))


def main() -> None:
    digits_sequence = map(int, input().strip())
    combinations_generator = LettersCombinationsGenerator(digits_sequence)
    combinations_iter = combinations_generator.generate()
    print(*combinations_iter)


if __name__ == '__main__':
    main()
