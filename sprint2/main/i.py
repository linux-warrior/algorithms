from __future__ import annotations

import abc
import re
from collections.abc import Iterable
from typing import Any, ClassVar


class MyQueueSized:
    max_size: int

    items: list[int]
    head_pos: int
    tail_pos: int
    size: int

    def __init__(self, *, max_size: int) -> None:
        self.max_size = max_size

        self.items = []
        self.head_pos = self.tail_pos = self.size = 0

    def get_size(self) -> int:
        return self.size

    def push(self, item: int) -> None:
        if len(self.items) < self.max_size:
            self.items.append(item)
            self.tail_pos += 1
            self.size += 1
            return

        if self.size == self.max_size:
            raise ValueError('Queue max size exceeded')

        if self.tail_pos == self.max_size:
            self.tail_pos = 0

        self.items[self.tail_pos] = item
        self.tail_pos += 1
        self.size += 1

    def pop(self) -> int:
        if not self.size:
            raise ValueError('Queue is empty')

        item = self.items[self.head_pos]
        self.head_pos += 1
        self.size -= 1

        if self.head_pos == self.max_size:
            self.head_pos = 0

            if self.tail_pos == self.max_size:
                self.tail_pos = 0

        return item

    def peek(self) -> int:
        if not self.size:
            raise ValueError('Queue is empty')

        return self.items[self.head_pos]


class MyQueueSizedCommand(abc.ABC):
    queue: MyQueueSized

    def __init__(self, queue: MyQueueSized) -> None:
        self.queue = queue

    @abc.abstractmethod
    def execute(self) -> str | None: ...


class SizeCommand(MyQueueSizedCommand):
    def execute(self) -> str:
        return str(self.queue.get_size())


class PushCommand(MyQueueSizedCommand):
    item: int

    def __init__(self, *args: Any, item: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.item = item

    def execute(self) -> str | None:
        try:
            self.queue.push(self.item)
        except ValueError:
            return 'error'

        return None


class PopCommand(MyQueueSizedCommand):
    def execute(self) -> str:
        try:
            item = self.queue.pop()
        except ValueError:
            return 'None'

        return str(item)


class PeekCommand(MyQueueSizedCommand):
    def execute(self) -> str:
        try:
            item = self.queue.peek()
        except ValueError:
            return 'None'

        return str(item)


class MyQueueSizedCommandParser(abc.ABC):
    command_pattern: ClassVar[str]
    command_re: re.Pattern[str]

    def __init__(self) -> None:
        self.command_re = re.compile(self.command_pattern)

    def parse(self, *, queue: MyQueueSized, command_str: str) -> MyQueueSizedCommand | None:
        command_match = self.command_re.fullmatch(command_str)
        if command_match is None:
            return None

        return self.create_command(queue=queue, command_match=command_match)

    @abc.abstractmethod
    def create_command(self,
                       *,
                       queue: MyQueueSized,
                       command_match: re.Match[str]) -> MyQueueSizedCommand: ...


class SizeCommandParser(MyQueueSizedCommandParser):
    command_pattern = r'size'

    def create_command(self,
                       *,
                       queue: MyQueueSized,
                       command_match: re.Match[str]) -> MyQueueSizedCommand:
        return SizeCommand(queue)


class PushCommandParser(MyQueueSizedCommandParser):
    command_pattern = r'push (-?\d+)'

    def create_command(self,
                       *,
                       queue: MyQueueSized,
                       command_match: re.Match[str]) -> MyQueueSizedCommand:
        return PushCommand(queue, item=int(command_match.group(1)))


class PopCommandParser(MyQueueSizedCommandParser):
    command_pattern = r'pop'

    def create_command(self,
                       *,
                       queue: MyQueueSized,
                       command_match: re.Match[str]) -> MyQueueSizedCommand:
        return PopCommand(queue)


class PeekCommandParser(MyQueueSizedCommandParser):
    command_pattern = r'peek'

    def create_command(self,
                       *,
                       queue: MyQueueSized,
                       command_match: re.Match[str]) -> MyQueueSizedCommand:
        return PeekCommand(queue)


class MyQueueSizedCommandExecutor:
    queue: MyQueueSized
    command_parsers: Iterable[MyQueueSizedCommandParser]

    def __init__(self, queue: MyQueueSized) -> None:
        self.queue = queue
        self.command_parsers = self.get_command_parsers()

    def get_command_parsers(self) -> Iterable[MyQueueSizedCommandParser]:
        return [
            SizeCommandParser(),
            PushCommandParser(),
            PopCommandParser(),
            PeekCommandParser(),
        ]

    def execute(self, command_str: str) -> str | None:
        for command_parser in self.command_parsers:
            command = command_parser.parse(queue=self.queue, command_str=command_str)
            if command is None:
                continue

            return command.execute()

        return None


def main() -> None:
    commands_count = int(input().strip())
    max_size = int(input().strip())

    queue = MyQueueSized(max_size=max_size)
    commands_executor = MyQueueSizedCommandExecutor(queue)

    for i in range(commands_count):
        command_str = input().strip()
        result = commands_executor.execute(command_str)

        if result is not None:
            print(result)


if __name__ == '__main__':
    main()
