from __future__ import annotations

import abc
import enum
from collections.abc import Mapping


class BracketType(enum.StrEnum):
    PARENTHESES = '()'
    SQUARE_BRACKETS = '[]'
    CURLY_BRACES = '{}'


class BracketSequenceException(Exception):
    pass


class InvalidToken(BracketSequenceException):
    pass


class BracketsDontMatch(BracketSequenceException):
    pass


class CloseBracketExpected(BracketSequenceException):
    pass


class BracketSequence:
    stack: list[BracketType]

    def __init__(self) -> None:
        self.stack = []

    def __bool__(self) -> bool:
        return bool(self.stack)

    def open_bracket(self, *, bracket_type: BracketType) -> None:
        self.stack.append(bracket_type)

    def close_bracket(self, *, bracket_type: BracketType) -> None:
        if not self.stack:
            raise BracketsDontMatch

        previous_bracket_type = self.stack[-1]

        if bracket_type != previous_bracket_type:
            raise BracketsDontMatch

        self.stack.pop()


class BracketToken(abc.ABC):
    bracket_type: BracketType

    def __init__(self,
                 *,
                 bracket_type: BracketType) -> None:
        self.bracket_type = bracket_type

    @abc.abstractmethod
    def process(self, *, sequence: BracketSequence) -> None: ...


class OpenBracketToken(BracketToken):
    def process(self, *, sequence: BracketSequence) -> None:
        sequence.open_bracket(bracket_type=self.bracket_type)


class CloseBracketToken(BracketToken):
    def process(self, *, sequence: BracketSequence) -> None:
        sequence.close_bracket(bracket_type=self.bracket_type)


class BracketSequenceParser:
    sequence: BracketSequence
    tokens: Mapping[str, BracketToken]

    def __init__(self) -> None:
        self.sequence = BracketSequence()
        self.tokens = self.get_tokens()

    def get_tokens(self) -> Mapping[str, BracketToken]:
        return {
            '(': OpenBracketToken(bracket_type=BracketType.PARENTHESES),
            ')': CloseBracketToken(bracket_type=BracketType.PARENTHESES),
            '[': OpenBracketToken(bracket_type=BracketType.SQUARE_BRACKETS),
            ']': CloseBracketToken(bracket_type=BracketType.SQUARE_BRACKETS),
            '{': OpenBracketToken(bracket_type=BracketType.CURLY_BRACES),
            '}': CloseBracketToken(bracket_type=BracketType.CURLY_BRACES),
        }

    def parse(self, bracket_str: str) -> None:
        self.sequence = BracketSequence()

        for bracket_char in bracket_str:
            token = self.tokens.get(bracket_char)
            if token is None:
                raise InvalidToken

            token.process(sequence=self.sequence)

        if self.sequence:
            raise CloseBracketExpected


def is_correct_bracket_seq(bracket_str: str) -> bool:
    sequence_parser = BracketSequenceParser()

    try:
        sequence_parser.parse(bracket_str)
    except BracketSequenceException:
        return False

    return True


def main() -> None:
    bracket_str = input().strip()
    print(is_correct_bracket_seq(bracket_str))


if __name__ == '__main__':
    main()
