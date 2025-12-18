from __future__ import annotations

import dataclasses
import functools
import operator
import sys
from collections.abc import Iterable, Iterator, Sequence, Callable


def get_longest_common_prefix(strings: Sequence[str]) -> str:
    common_prefix_tool = CommonPrefixTool(strings)
    return common_prefix_tool.get_longest_common_prefix()


class CommonPrefixTool:
    strings: Sequence[str]

    __slots__ = (
        'strings',
    )

    def __init__(self, strings: Sequence[str]) -> None:
        self.strings = strings

    def get_longest_common_prefix(self) -> str:
        return ''.join(self._get_longest_common_prefix_chars())

    def _get_longest_common_prefix_chars(self) -> Iterable[str]:
        strings_count = len(self.strings)

        if not strings_count:
            return

        char_iter_list = [unpack_chars(s) for s in self.strings]
        first_char_iter = char_iter_list[0]

        while True:
            try:
                char = next(first_char_iter)
            except StopIteration:
                return

            for i in range(1, strings_count):
                try:
                    other_char = next(char_iter_list[i])
                except StopIteration:
                    return

                if char != other_char:
                    return

            yield char


def unpack_chars(s: str) -> Iterator[str]:
    unpack_tool = UnpackTool(s)
    return unpack_tool.unpack_chars()


class Repetition:
    start_pos: int
    count: int
    index: int

    __slots__ = (
        'start_pos',
        'count',
        'index',
    )

    def __init__(self, *, start_pos: int, count: int) -> None:
        self.start_pos = start_pos
        self.count = count
        self.index = 0

    def get_start_pos(self) -> int:
        return self.start_pos

    def next(self) -> None:
        self.index += 1

    def has_finished(self) -> bool:
        return self.index >= self.count


class RepetitionsStack:
    repetitions: list[Repetition]

    __slots__ = (
        'repetitions',
    )

    def __init__(self) -> None:
        self.repetitions = []

    def push(self, repetition: Repetition) -> None:
        self.repetitions.append(repetition)

    def pop(self) -> None:
        if not self.repetitions:
            return

        self.repetitions.pop()

    def get_current(self) -> Repetition | None:
        if not self.repetitions:
            return None

        return self.repetitions[-1]


@dataclasses.dataclass(kw_only=True, slots=True)
class ParseTokenResult:
    new_pos: int


type TokenCheck = Callable[[str], bool]
type TokenParser = Callable[[str, int], ParseTokenResult | None]


class UnpackTool:
    s: str
    repetitions_stack: RepetitionsStack
    repetition_count: int
    token_parsers: Iterable[tuple[TokenCheck, TokenParser]]

    __slots__ = (
        's',
        'repetitions_stack',
        'repetition_count',
        'token_parsers',
    )

    def __init__(self, s: str) -> None:
        self.s = s
        self.repetitions_stack = RepetitionsStack()
        self.repetition_count = 0
        self.token_parsers = self._get_token_parsers()

    def _get_token_parsers(self) -> Iterable[tuple[TokenCheck, TokenParser]]:
        return [
            (str.isdigit, self._parse_repetition_count),
            (functools.partial(operator.eq, '['), self._parse_repetition_start),
            (functools.partial(operator.eq, ']'), self._parse_repetition_end),
        ]

    def unpack_chars(self) -> Iterator[str]:
        self.repetitions_stack = RepetitionsStack()
        self.repetition_count = 0

        s_length = len(self.s)
        pos = 0

        while pos < s_length:
            char = self.s[pos]
            is_token = False
            parse_token_result: ParseTokenResult | None = None

            for token_check, token_parser in self.token_parsers:
                if not token_check(char):
                    continue

                is_token = True
                parse_token_result = token_parser(char, pos)
                break

            if not is_token:
                pos += 1
                yield char
                continue

            if parse_token_result is None:
                pos += 1
                continue

            pos = parse_token_result.new_pos

    # noinspection PyUnusedLocal
    def _parse_repetition_count(self, char: str, pos: int) -> ParseTokenResult | None:
        try:
            self.repetition_count = int(char)
        except ValueError:
            return None

        return None

    # noinspection PyUnusedLocal
    def _parse_repetition_start(self, char: str, pos: int) -> ParseTokenResult | None:
        self.repetitions_stack.push(Repetition(
            start_pos=pos + 1,
            count=self.repetition_count,
        ))
        self.repetition_count = 0

        return None

    # noinspection PyUnusedLocal
    def _parse_repetition_end(self, char: str, pos: int) -> ParseTokenResult | None:
        current_repetition = self.repetitions_stack.get_current()

        if current_repetition is None:
            return None

        current_repetition.next()

        if current_repetition.has_finished():
            self.repetitions_stack.pop()
            return None

        start_pos = current_repetition.get_start_pos()

        return ParseTokenResult(
            new_pos=start_pos,
        )


def read_strings(count: int) -> Iterable[str]:
    for i in range(count):
        yield sys.stdin.readline().strip()


def main() -> None:
    strings_count = int(input().strip())
    strings = list(read_strings(strings_count))

    print(get_longest_common_prefix(strings))


if __name__ == '__main__':
    main()
