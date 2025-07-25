# https://contest.yandex.ru/contest/22781/run-report/140477565/
#
# -- Принцип работы --
#
# Калькулятор вычисляет значения арифметических выражений, записанных в обратной польской нотации.
# Для временного сохранения чисел, которые содержатся в арифметическом выражении, используется стек,
# изначально пустой. Строка символов, переданная в калькулятор, разбивается на токены, отделенные
# друг от друга пробелами. Далее для каждого токена выполняется одна из следующих команд:
#
# * Если было получено число, то оно помещается на вершину стека.
# * Если был получен знак арифметической операции, то из стека извлекаются два последних числа и
#   вычисляется результат операции, который помещается обратно в стек.
#
# После того как все токены были обработаны, результат арифметического выражения расположен на вершине
# стека.
#
# -- Доказательство корректности --
#
# Если арифметическое выражение не содержит лишних чисел, то результатом будет единственный элемент,
# оставшийся в стеке после обработки всех токенов. В следующих случаях программа завершит работу с
# исключением `ValueError`:
#
# * Исходная строка содержит токен, который не является ни операцией, ни числом.
# * В строке недостаточно чисел для выполнения всех арифметических операций.
#
# -- Временная сложность --
#
# Поскольку обработка каждого токена выполняется за фиксированное число операций, то вычислительная
# сложность определения значения арифметического выражения составляет `O(n)`, где `n` — количество
# токенов в исходной строке.
#
# -- Пространственная сложность --
#
# В худшем возможном варианте все операнды расположены в начале арифметического выражения, а за ними
# следуют операции. В этом случае необходимо будет поместить в стек сразу все числа из выражения.
# Тогда пространственная сложность составит `O(n)`.

from __future__ import annotations

import abc
import re
from collections.abc import Mapping, Iterable
from typing import Any, ClassVar


class CalculatorStack:
    values: list[int]

    def __init__(self) -> None:
        self.values = []

    def push(self, value: int) -> None:
        self.values.append(value)

    def pop(self) -> int:
        if not self.values:
            raise ValueError('Stack is empty')

        return self.values.pop()

    def get_result(self) -> int:
        if not self.values:
            raise ValueError('Stack is empty')

        return self.values[-1]


class CalculatorCommand(abc.ABC):
    stack: CalculatorStack

    def __init__(self, stack: CalculatorStack) -> None:
        self.stack = stack

    @abc.abstractmethod
    def execute(self) -> None: ...


class ValueCommand(CalculatorCommand):
    value: int

    def __init__(self, *args: Any, value: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.value = value

    def execute(self) -> None:
        self.stack.push(self.value)


class OperationCommand(CalculatorCommand):
    def execute(self) -> None:
        b = self.stack.pop()
        a = self.stack.pop()
        result = self.calculate(a, b)
        self.stack.push(result)

    @abc.abstractmethod
    def calculate(self, a: int, b: int) -> int: ...


class AddCommand(OperationCommand):
    def calculate(self, a: int, b: int) -> int:
        return a + b


class SubtractCommand(OperationCommand):
    def calculate(self, a: int, b: int) -> int:
        return a - b


class MultiplyCommand(OperationCommand):
    def calculate(self, a: int, b: int) -> int:
        return a * b


class DivideCommand(OperationCommand):
    def calculate(self, a: int, b: int) -> int:
        return a // b


class CalculatorCommandParser(abc.ABC):
    token_pattern: ClassVar[str]
    token_re: re.Pattern[str]

    def __init__(self) -> None:
        self.token_re = re.compile(self.token_pattern)

    def parse(self, *, stack: CalculatorStack, token: str) -> CalculatorCommand | None:
        token_match = self.token_re.fullmatch(token)
        if token_match is None:
            return None

        return self.create_command(stack=stack, token_match=token_match)

    @abc.abstractmethod
    def create_command(self,
                       *,
                       stack: CalculatorStack,
                       token_match: re.Match[str]) -> CalculatorCommand: ...


class ValueCommandParser(CalculatorCommandParser):
    token_pattern = r'-?\d+'

    def create_command(self,
                       *,
                       stack: CalculatorStack,
                       token_match: re.Match[str]) -> CalculatorCommand:
        return ValueCommand(stack, value=int(token_match.group()))


class OperationCommandParser(CalculatorCommandParser):
    token_pattern = r'[+\-*/]'
    command_classes: ClassVar[Mapping[str, type[OperationCommand]]] = {
        '+': AddCommand,
        '-': SubtractCommand,
        '*': MultiplyCommand,
        '/': DivideCommand,
    }

    def create_command(self,
                       *,
                       stack: CalculatorStack,
                       token_match: re.Match[str]) -> CalculatorCommand:
        operation_char = token_match.group()
        command_class = self.command_classes.get(operation_char)

        if command_class is None:
            raise ValueError('Invalid operation symbol')

        return command_class(stack)


class Calculator:
    stack: CalculatorStack
    command_parsers: Iterable[CalculatorCommandParser]

    def __init__(self) -> None:
        self.stack = CalculatorStack()
        self.command_parsers = self.get_command_parsers()

    def get_command_parsers(self) -> Iterable[CalculatorCommandParser]:
        return [
            ValueCommandParser(),
            OperationCommandParser(),
        ]

    def calculate(self, tokens_str: str) -> int:
        self.stack = CalculatorStack()

        for token in tokens_str.split():
            command = self._parse_token(token)
            command.execute()

        return self.stack.get_result()

    def _parse_token(self, token: str) -> CalculatorCommand:
        for command_parser in self.command_parsers:
            command = command_parser.parse(stack=self.stack, token=token)
            if command is None:
                continue

            return command

        raise ValueError('Invalid token')


def main() -> None:
    tokens_str = input().strip()

    calculator = Calculator()
    result = calculator.calculate(tokens_str)
    print(result)


if __name__ == '__main__':
    main()
