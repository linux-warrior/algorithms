from __future__ import annotations

import abc
import re
from collections.abc import Iterable
from typing import Any, ClassVar


class StackMax:
    items: list[int]

    def __init__(self, items: Iterable[int] | None = None) -> None:
        self.items = list(items or [])

    def __bool__(self) -> bool:
        return bool(self.items)

    def push(self, item: int) -> None:
        self.items.append(item)

    def pop(self) -> int:
        if not self:
            raise ValueError('Stack is empty')

        return self.items.pop()

    def get_max(self) -> int | None:
        if not self:
            return None

        return max(self.items)


class StackMaxCommand(abc.ABC):
    stack: StackMax

    def __init__(self, stack: StackMax) -> None:
        self.stack = stack

    def execute(self) -> str | None:
        return None


class PushCommand(StackMaxCommand):
    item: int

    def __init__(self, *args: Any, item: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.item = item

    def execute(self) -> None:
        self.stack.push(self.item)


class PopCommand(StackMaxCommand):
    def execute(self) -> str | None:
        try:
            self.stack.pop()
        except ValueError:
            return 'error'

        return None


class GetMaxCommand(StackMaxCommand):
    def execute(self) -> str:
        return str(self.stack.get_max())


class StackMaxCommandParser(abc.ABC):
    command_pattern: ClassVar[str]
    command_re: re.Pattern[str]

    def __init__(self) -> None:
        self.command_re = re.compile(self.command_pattern)

    def parse(self, *, stack: StackMax, command_str: str) -> StackMaxCommand | None:
        command_match = self.command_re.match(command_str)
        if command_match is None:
            return None

        return self.create_command(stack=stack, command_match=command_match)

    @abc.abstractmethod
    def create_command(self,
                       *,
                       stack: StackMax,
                       command_match: re.Match[str]) -> StackMaxCommand: ...


class PushCommandParser(StackMaxCommandParser):
    command_pattern = r'^push (-?\d+)$'

    def create_command(self,
                       *,
                       stack: StackMax,
                       command_match: re.Match[str]) -> StackMaxCommand:
        return PushCommand(stack, item=int(command_match.group(1)))


class PopCommandParser(StackMaxCommandParser):
    command_pattern = r'^pop$'

    def create_command(self,
                       *,
                       stack: StackMax,
                       command_match: re.Match[str]) -> StackMaxCommand:
        return PopCommand(stack)


class GetMaxCommandParser(StackMaxCommandParser):
    command_pattern = r'^get_max$'

    def create_command(self,
                       *,
                       stack: StackMax,
                       command_match: re.Match[str]) -> StackMaxCommand:
        return GetMaxCommand(stack)


class StackMaxCommandsExecutor:
    stack: StackMax
    command_parsers: Iterable[StackMaxCommandParser]

    def __init__(self, stack: StackMax) -> None:
        self.stack = stack
        self.command_parsers = self.get_command_parsers()

    def get_command_parsers(self) -> Iterable[StackMaxCommandParser]:
        return [
            PushCommandParser(),
            PopCommandParser(),
            GetMaxCommandParser(),
        ]

    def execute(self, command_str: str) -> str | None:
        for command_parser in self.command_parsers:
            command = command_parser.parse(stack=self.stack, command_str=command_str)
            if command is None:
                continue

            return command.execute()

        return None


def main() -> None:
    stack = StackMax()
    commands_executor = StackMaxCommandsExecutor(stack)
    commands_count = int(input().strip())

    for i in range(commands_count):
        command_str = input().strip()
        result = commands_executor.execute(command_str)

        if result is not None:
            print(result)


if __name__ == '__main__':
    main()
