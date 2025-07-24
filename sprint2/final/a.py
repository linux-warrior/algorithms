# https://contest.yandex.ru/contest/22781/run-report/140351512/
#
# -- Принцип работы --
#
# Для хранения элементов дека используется кольцевой буфер, причем память под максимально допустимое
# число элементов выделяется заранее при инициализации структуры данных. Для обозначения начала и
# конца очереди были созданы два указателя на ячейки буфера, содержащие соответственно индекс первого
# элемента и индекс свободной ячейки, расположенной сразу же за последним элементом.
#
# При добавлении элементов в дек, как и при их удалении, указатель на начало или конец очереди смещается
# на соседний элемент буфера. В случае выхода указателя за левую или правую границу буфера, указателю
# присваивается крайнее допустимое положение с противоположной стороны буфера. Таким образом, при
# работе с деком перемещение указателей на элементы буфера выполняется как бы по кольцу.
#
# -- Доказательство корректности --
#
# Принцип работы с кольцевым буфером по сути аналогичен использованию буфера бесконечной длины, за
# исключением того, что индексы, указывающие на первый и последний элементы очереди, считаются по
# модулю длины буфера. Таким образом, если переполнения буфера не происходит, то добавление и удаление
# элементов дека должно выполняться корректно.
#
# -- Временная сложность --
#
# Так как добавление и удаление элементов с обеих сторон дека выполняется за фиксированное число
# операций, то вычислительная сложность этих методов составляет `O(1)`.
#
# -- Пространственная сложность --
#
# Поскольку память под буфер выделяется заранее, то пространственная сложность структуры данных
# составляет `O(max_size)`, где `max_size` — максимальный размер дека.

from __future__ import annotations

import abc
import re
from collections.abc import Iterable
from typing import Any, ClassVar


class Deque:
    max_size: int

    items: list[int]
    head_pos: int
    tail_pos: int
    size: int

    def __init__(self, *, max_size: int) -> None:
        self.max_size = max_size

        self.items = [0] * self.max_size
        self.head_pos = self.tail_pos = self.size = 0

    def push_back(self, item: int) -> None:
        if self.size == self.max_size:
            raise ValueError('Deque max size exceeded')

        if self.tail_pos == self.max_size:
            self.tail_pos = 0

        self.items[self.tail_pos] = item
        self.tail_pos += 1
        self.size += 1

    def push_front(self, item: int) -> None:
        if self.size == self.max_size:
            raise ValueError('Deque max size exceeded')

        if self.head_pos == 0:
            self.head_pos = self.max_size

        self.head_pos -= 1
        self.items[self.head_pos] = item
        self.size += 1

    def pop_back(self) -> int:
        if self.size == 0:
            raise ValueError('Deque is empty')

        self.tail_pos -= 1
        item = self.items[self.tail_pos]
        self.size -= 1

        if self.tail_pos == 0 and self.size != 0:
            self.tail_pos = self.max_size

        return item

    def pop_front(self) -> int:
        if self.size == 0:
            raise ValueError('Deque is empty')

        item = self.items[self.head_pos]
        self.head_pos += 1
        self.size -= 1

        if self.head_pos == self.max_size:
            self.head_pos = 0

            if self.size == 0:
                self.tail_pos = 0

        return item


class DequeCommand(abc.ABC):
    deque: Deque

    def __init__(self, deque: Deque) -> None:
        self.deque = deque

    @abc.abstractmethod
    def execute(self) -> str | None: ...


class PushBackCommand(DequeCommand):
    item: int

    def __init__(self, *args: Any, item: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.item = item

    def execute(self) -> str | None:
        try:
            self.deque.push_back(self.item)
        except ValueError:
            return 'error'

        return None


class PushFrontCommand(DequeCommand):
    item: int

    def __init__(self, *args: Any, item: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.item = item

    def execute(self) -> str | None:
        try:
            self.deque.push_front(self.item)
        except ValueError:
            return 'error'

        return None


class PopBackCommand(DequeCommand):
    def execute(self) -> str:
        try:
            item = self.deque.pop_back()
        except ValueError:
            return 'error'

        return str(item)


class PopFrontCommand(DequeCommand):
    def execute(self) -> str:
        try:
            item = self.deque.pop_front()
        except ValueError:
            return 'error'

        return str(item)


class DequeCommandParser(abc.ABC):
    command_pattern: ClassVar[str]
    command_re: re.Pattern[str]

    def __init__(self) -> None:
        self.command_re = re.compile(self.command_pattern)

    def parse(self, *, deque: Deque, command_str: str) -> DequeCommand | None:
        command_match = self.command_re.fullmatch(command_str)
        if command_match is None:
            return None

        return self.create_command(deque=deque, command_match=command_match)

    @abc.abstractmethod
    def create_command(self,
                       *,
                       deque: Deque,
                       command_match: re.Match[str]) -> DequeCommand: ...


class PushBackCommandParser(DequeCommandParser):
    command_pattern = r'push_back (-?\d+)'

    def create_command(self,
                       *,
                       deque: Deque,
                       command_match: re.Match[str]) -> DequeCommand:
        return PushBackCommand(deque, item=int(command_match.group(1)))


class PushFrontCommandParser(DequeCommandParser):
    command_pattern = r'push_front (-?\d+)'

    def create_command(self,
                       *,
                       deque: Deque,
                       command_match: re.Match[str]) -> DequeCommand:
        return PushFrontCommand(deque, item=int(command_match.group(1)))


class PopBackCommandParser(DequeCommandParser):
    command_pattern = r'pop_back'

    def create_command(self,
                       *,
                       deque: Deque,
                       command_match: re.Match[str]) -> DequeCommand:
        return PopBackCommand(deque)


class PopFrontCommandParser(DequeCommandParser):
    command_pattern = r'pop_front'

    def create_command(self,
                       *,
                       deque: Deque,
                       command_match: re.Match[str]) -> DequeCommand:
        return PopFrontCommand(deque)


class DequeCommandExecutor:
    deque: Deque
    command_parsers: Iterable[DequeCommandParser]

    def __init__(self, deque: Deque) -> None:
        self.deque = deque
        self.command_parsers = self.get_command_parsers()

    def get_command_parsers(self) -> Iterable[DequeCommandParser]:
        return [
            PushBackCommandParser(),
            PushFrontCommandParser(),
            PopBackCommandParser(),
            PopFrontCommandParser(),
        ]

    def execute(self, command_str: str) -> str | None:
        for command_parser in self.command_parsers:
            command = command_parser.parse(deque=self.deque, command_str=command_str)
            if command is None:
                continue

            return command.execute()

        return None


def main() -> None:
    commands_count = int(input().strip())
    max_size = int(input().strip())

    deque = Deque(max_size=max_size)
    commands_executor = DequeCommandExecutor(deque)

    for i in range(commands_count):
        command_str = input().strip()
        result = commands_executor.execute(command_str)

        if result is not None:
            print(result)


if __name__ == '__main__':
    main()
