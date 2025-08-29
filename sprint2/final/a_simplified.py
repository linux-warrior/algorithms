# https://contest.yandex.ru/contest/22781/run-report/141639047/
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

import re
from collections.abc import Iterable, Callable


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

        self.items[self.tail_pos] = item
        self.tail_pos = (self.tail_pos + 1) % self.max_size
        self.size += 1

    def push_front(self, item: int) -> None:
        if self.size == self.max_size:
            raise ValueError('Deque max size exceeded')

        self.head_pos = (self.head_pos - 1) % self.max_size
        self.items[self.head_pos] = item
        self.size += 1

    def pop_back(self) -> int:
        if self.size == 0:
            raise ValueError('Deque is empty')

        self.tail_pos = (self.tail_pos - 1) % self.max_size
        item = self.items[self.tail_pos]
        self.size -= 1

        return item

    def pop_front(self) -> int:
        if self.size == 0:
            raise ValueError('Deque is empty')

        item = self.items[self.head_pos]
        self.head_pos = (self.head_pos + 1) % self.max_size
        self.size -= 1

        return item


type DequeCommandParser = Callable[[re.Match[str]], str | None]


class DequeCommandsExecutor:
    deque: Deque
    command_parsers: Iterable[tuple[re.Pattern[str], DequeCommandParser]]

    def __init__(self, deque: Deque) -> None:
        self.deque = deque
        self.command_parsers = self.get_command_parsers()

    def get_command_parsers(self) -> Iterable[tuple[re.Pattern[str], DequeCommandParser]]:
        return [(
            re.compile(command_pattern),
            command_parser,
        ) for command_pattern, command_parser in [
            (r'push_back (-?\d+)', self._parse_push_back),
            (r'push_front (-?\d+)', self._parse_push_front),
            (r'pop_back', self._parse_pop_back),
            (r'pop_front', self._parse_pop_front),
        ]]

    def execute(self, command_str: str) -> str | None:
        for command_re, command_parser in self.command_parsers:
            command_match = command_re.fullmatch(command_str)
            if command_match is None:
                continue

            try:
                return command_parser(command_match)
            except ValueError:
                return 'error'

        return None

    def _parse_push_back(self, command_match: re.Match[str]) -> None:
        item = int(command_match.group(1))
        self.deque.push_back(item)

    def _parse_push_front(self, command_match: re.Match[str]) -> None:
        item = int(command_match.group(1))
        self.deque.push_front(item)

    # noinspection PyUnusedLocal
    def _parse_pop_back(self, command_match: re.Match[str]) -> str:
        item = self.deque.pop_back()
        return str(item)

    # noinspection PyUnusedLocal
    def _parse_pop_front(self, command_match: re.Match[str]) -> str:
        item = self.deque.pop_front()
        return str(item)


def main() -> None:
    commands_count = int(input().strip())
    max_size = int(input().strip())

    deque = Deque(max_size=max_size)
    commands_executor = DequeCommandsExecutor(deque)

    for i in range(commands_count):
        command_str = input().strip()
        result = commands_executor.execute(command_str)

        if result is not None:
            print(result)


if __name__ == '__main__':
    main()
