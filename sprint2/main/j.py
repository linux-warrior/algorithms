from __future__ import annotations

import abc
import dataclasses
import re
from collections.abc import Iterable
from typing import Any, ClassVar


@dataclasses.dataclass(kw_only=True)
class QueueItem:
    value: int
    next_item: QueueItem | None = None


class Queue:
    head: QueueItem | None
    tail: QueueItem | None
    size: int

    def __init__(self) -> None:
        self.head = self.tail = None
        self.size = 0

    def get_size(self) -> int:
        return self.size

    def put(self, value: int) -> None:
        tail = QueueItem(value=value)

        if self.tail is None:
            self.head = self.tail = tail
        else:
            self.tail.next_item = tail
            self.tail = tail

        self.size += 1

    def get(self) -> int:
        if self.head is None:
            raise ValueError('Queue is empty')

        value = self.head.value
        self.head = self.head.next_item
        self.size -= 1

        if self.head is None:
            self.tail = None

        return value


class QueueCommand(abc.ABC):
    queue: Queue

    def __init__(self, queue: Queue) -> None:
        self.queue = queue

    @abc.abstractmethod
    def execute(self) -> str | None: ...


class SizeCommand(QueueCommand):
    def execute(self) -> str:
        return str(self.queue.get_size())


class PutCommand(QueueCommand):
    value: int

    def __init__(self, *args: Any, value: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.value = value

    def execute(self) -> None:
        self.queue.put(self.value)


class GetCommand(QueueCommand):
    def execute(self) -> str:
        try:
            value = self.queue.get()
        except ValueError:
            return 'error'

        return str(value)


class QueueCommandParser(abc.ABC):
    command_pattern: ClassVar[str]
    command_re: re.Pattern[str]

    def __init__(self) -> None:
        self.command_re = re.compile(self.command_pattern)

    def parse(self, *, queue: Queue, command_str: str) -> QueueCommand | None:
        command_match = self.command_re.fullmatch(command_str)
        if command_match is None:
            return None

        return self.create_command(queue=queue, command_match=command_match)

    @abc.abstractmethod
    def create_command(self,
                       *,
                       queue: Queue,
                       command_match: re.Match[str]) -> QueueCommand: ...


class SizeCommandParser(QueueCommandParser):
    command_pattern = r'size'

    def create_command(self,
                       *,
                       queue: Queue,
                       command_match: re.Match[str]) -> QueueCommand:
        return SizeCommand(queue)


class PutCommandParser(QueueCommandParser):
    command_pattern = r'put (-?\d+)'

    def create_command(self,
                       *,
                       queue: Queue,
                       command_match: re.Match[str]) -> QueueCommand:
        return PutCommand(queue, value=int(command_match.group(1)))


class GetCommandParser(QueueCommandParser):
    command_pattern = r'get'

    def create_command(self,
                       *,
                       queue: Queue,
                       command_match: re.Match[str]) -> QueueCommand:
        return GetCommand(queue)


class QueueCommandExecutor:
    queue: Queue
    command_parsers: Iterable[QueueCommandParser]

    def __init__(self, queue: Queue) -> None:
        self.queue = queue
        self.command_parsers = self.get_command_parsers()

    def get_command_parsers(self) -> Iterable[QueueCommandParser]:
        return [
            SizeCommandParser(),
            PutCommandParser(),
            GetCommandParser(),
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

    queue = Queue()
    commands_executor = QueueCommandExecutor(queue)

    for i in range(commands_count):
        command_str = input().strip()
        result = commands_executor.execute(command_str)

        if result is not None:
            print(result)


if __name__ == '__main__':
    main()
