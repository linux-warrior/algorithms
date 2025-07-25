# https://contest.yandex.ru/contest/22781/run-report/140478282/
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

import operator
import re
from collections.abc import Mapping, Iterable, Callable


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


type CalculatorCommandParser = Callable[[re.Match[str]], None]
type OperationCommand = Callable[[int, int], int]


class Calculator:
    stack: CalculatorStack
    command_parsers: Iterable[tuple[re.Pattern[str], CalculatorCommandParser]]
    operations: Mapping[str, OperationCommand] = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.floordiv,
    }

    def __init__(self) -> None:
        self.stack = CalculatorStack()
        self.command_parsers = self.get_command_parsers()

    def get_command_parsers(self) -> Iterable[tuple[re.Pattern[str], CalculatorCommandParser]]:
        return [(
            re.compile(token_pattern),
            command_parser,
        ) for token_pattern, command_parser in [
            (r'-?\d+', self._parse_value),
            (r'[+\-*/]', self._parse_operation),
        ]]

    def calculate(self, tokens_str: str) -> int:
        self.stack = CalculatorStack()

        for token in tokens_str.split():
            self._parse_token(token)

        return self.stack.get_result()

    def _parse_token(self, token: str) -> None:
        for token_re, command_parser in self.command_parsers:
            token_match = token_re.fullmatch(token)
            if token_match is None:
                continue

            command_parser(token_match)
            return

        raise ValueError('Invalid token')

    def _parse_value(self, token_match: re.Match[str]) -> None:
        value = int(token_match.group())
        self.stack.push(value)

    def _parse_operation(self, token_match: re.Match[str]) -> None:
        operation_char = token_match.group()
        operation = self.operations.get(operation_char)

        if operation is None:
            raise ValueError('Invalid operation symbol')

        b = self.stack.pop()
        a = self.stack.pop()
        result = operation(a, b)
        self.stack.push(result)


def main() -> None:
    tokens_str = input().strip()

    calculator = Calculator()
    result = calculator.calculate(tokens_str)
    print(result)


if __name__ == '__main__':
    main()
