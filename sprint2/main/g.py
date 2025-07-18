from __future__ import annotations

import abc
import re
from collections.abc import Iterable
from typing import Any, ClassVar


class StackMaxEffective:
    items: list[int]
    max_items: list[int]

    def __init__(self, items: Iterable[int] | None = None) -> None:
        self.items = []
        self.max_items = []

        for item in items or []:
            self.push(item)

    def __bool__(self) -> bool:
        return bool(self.items)

    def push(self, item: int) -> None:
        self.items.append(item)

        if not self.max_items or item >= self.max_items[-1]:
            self.max_items.append(item)

    def pop(self) -> int:
        if not self:
            raise ValueError('Stack is empty')

        item = self.items.pop()

        if item == self.max_items[-1]:
            self.max_items.pop()

        return item

    def top(self) -> int:
        if not self:
            raise ValueError('Stack is empty')

        return self.items[-1]

    def get_max(self) -> int | None:
        if not self:
            return None

        return self.max_items[-1]


class StackMaxEffectiveCommand(abc.ABC):
    stack: StackMaxEffective

    def __init__(self, stack: StackMaxEffective) -> None:
        self.stack = stack

    def execute(self) -> str | None:
        return None


class PushCommand(StackMaxEffectiveCommand):
    item: int

    def __init__(self, *args: Any, item: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.item = item

    def execute(self) -> None:
        self.stack.push(self.item)


class PopCommand(StackMaxEffectiveCommand):
    def execute(self) -> str | None:
        try:
            self.stack.pop()
        except ValueError:
            return 'error'

        return None


class TopCommand(StackMaxEffectiveCommand):
    def execute(self) -> str | None:
        try:
            item = self.stack.top()
        except ValueError:
            return 'error'

        return str(item)


class GetMaxCommand(StackMaxEffectiveCommand):
    def execute(self) -> str:
        return str(self.stack.get_max())


class StackMaxEffectiveCommandParser(abc.ABC):
    command_pattern: ClassVar[str]
    command_re: re.Pattern[str]

    def __init__(self) -> None:
        self.command_re = re.compile(self.command_pattern)

    def parse(self, *, stack: StackMaxEffective, command_str: str) -> StackMaxEffectiveCommand | None:
        command_match = self.command_re.match(command_str)
        if command_match is None:
            return None

        return self.create_command(stack=stack, command_match=command_match)

    @abc.abstractmethod
    def create_command(self,
                       *,
                       stack: StackMaxEffective,
                       command_match: re.Match[str]) -> StackMaxEffectiveCommand: ...


class PushCommandParser(StackMaxEffectiveCommandParser):
    command_pattern = r'^push (-?\d+)$'

    def create_command(self,
                       *,
                       stack: StackMaxEffective,
                       command_match: re.Match[str]) -> StackMaxEffectiveCommand:
        return PushCommand(stack, item=int(command_match.group(1)))


class PopCommandParser(StackMaxEffectiveCommandParser):
    command_pattern = r'^pop$'

    def create_command(self,
                       *,
                       stack: StackMaxEffective,
                       command_match: re.Match[str]) -> StackMaxEffectiveCommand:
        return PopCommand(stack)


class TopCommandParser(StackMaxEffectiveCommandParser):
    command_pattern = r'^top$'

    def create_command(self,
                       *,
                       stack: StackMaxEffective,
                       command_match: re.Match[str]) -> StackMaxEffectiveCommand:
        return TopCommand(stack)


class GetMaxCommandParser(StackMaxEffectiveCommandParser):
    command_pattern = r'^get_max$'

    def create_command(self,
                       *,
                       stack: StackMaxEffective,
                       command_match: re.Match[str]) -> StackMaxEffectiveCommand:
        return GetMaxCommand(stack)


class StackMaxEffectiveCommandsExecutor:
    stack: StackMaxEffective
    command_parsers: Iterable[StackMaxEffectiveCommandParser]

    def __init__(self, stack: StackMaxEffective) -> None:
        self.stack = stack
        self.command_parsers = self.get_command_parsers()

    def get_command_parsers(self) -> Iterable[StackMaxEffectiveCommandParser]:
        return [
            PushCommandParser(),
            PopCommandParser(),
            TopCommandParser(),
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
    stack = StackMaxEffective()
    commands_executor = StackMaxEffectiveCommandsExecutor(stack)
    commands_count = int(input().strip())

    for i in range(commands_count):
        command_str = input().strip()
        result = commands_executor.execute(command_str)

        if result is not None:
            print(result)


if __name__ == '__main__':
    main()
