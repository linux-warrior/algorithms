from __future__ import annotations

import dataclasses
from collections.abc import Iterable


@dataclasses.dataclass(kw_only=True)
class BracketSequenceState:
    sequence: str = ''
    open_count: int = 0
    close_count: int = 0


class BracketSequenceGenerator:
    length: int
    open_char: str
    close_char: str

    def __init__(self,
                 length: int,
                 *,
                 open_char: str = '(',
                 close_char: str = ')') -> None:
        self.length = length
        self.open_char = open_char
        self.close_char = close_char

    def generate(self) -> Iterable[str]:
        yield from self._generate(state=BracketSequenceState())

    def _generate(self, *, state: BracketSequenceState) -> Iterable[str]:
        if state.open_count == self.length and state.close_count == self.length:
            yield state.sequence

        if state.open_count < self.length:
            yield from self._generate(state=BracketSequenceState(
                sequence=state.sequence + self.open_char,
                open_count=state.open_count + 1,
                close_count=state.close_count,
            ))

        if state.close_count < state.open_count:
            yield from self._generate(state=BracketSequenceState(
                sequence=state.sequence + self.close_char,
                open_count=state.open_count,
                close_count=state.close_count + 1,
            ))


def main() -> None:
    length = int(input().strip())
    sequence_generator = BracketSequenceGenerator(length)

    for sequence in sequence_generator.generate():
        print(sequence)


if __name__ == '__main__':
    main()
