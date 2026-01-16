# https://contest.yandex.ru/contest/25070/run-report/155283809/
#
# -- Принцип работы --
#
# В данной задаче реализован поиск и подсчет площадей островов на карте, представляющей собой таблицу,
# ячейки которой содержат воду (`.`) или землю (`#`). Карта хранится в поле экземпляра класса `Grid`
# в виде массива строк. Метод `Grid.find_islands()` возвращает общее количество островов и площадь
# самого большого из них.
#
# При запуске алгоритма мы создаем двумерный массив уже посещенных ячеек и очередь координат ячеек,
# для которых необходимо будет проверить соседние ячейки по горизонтали и вертикали. Далее мы начинаем
# последовательный обход всех ячеек карты. Если текущая ячейка еще не посещена и является землей, то
# мы начинаем обработку острова и сбрасываем значение площади. Далее мы обрабатываем стартовую ячейку
# острова: отмечаем ее как посещенную, добавляем в очередь и увеличиваем значение площади на единицу.
# Затем мы запускаем цикл, в каждой итерации которого мы извлекаем из очереди одну ячейку и последовательно
# проверяем ячейки, соседние с данной. Если соседняя ячейка еще не посещена и является землей, то мы
# обрабатываем ее аналогично первой ячейке острова. И так мы продолжаем до тех пор, пока очередь
# координат ячеек не окажется пустой. В конце обработки острова мы обновляем переменные, хранящие
# количество островов и максимальное значение площади.
#
# -- Доказательство корректности --
#
# Карту из задачи можно представить в виде графа, вершины которого расположены в ячейках, являющихся
# землей, а ребра соединяют соседние вершины по вертикали и горизонтали. Тогда принцип работы алгоритма
# будет аналогичен нахождению компонент связности в данном графе с помощью поиска в ширину (BFS).
#
# -- Временная сложность --
#
# Временная сложность алгоритма пропорциональна количеству ячеек карты и составляет `O(width · height)`,
# где `width` — ширина, а `height` — высота карты.
#
# -- Пространственная сложность --
#
# Пространственная сложность алгоритма составляет `O(width · height)`, поскольку во время его работы
# создается массив, хранящий флаг посещения каждой ячейки, и очередь координат ячеек.

from __future__ import annotations

import dataclasses
import sys
from collections import deque
from collections.abc import Iterable, Sequence
from typing import Self

type Vector = tuple[int, int]

DIRECTIONS: Sequence[Vector] = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]

type Tile = str
type TilesRow = str

TILE_WATER = '.'
TILE_LAND = '#'


class Grid:
    tiles: list[TilesRow]
    width: int
    height: int

    __slots__ = (
        'tiles',
        'width',
        'height',
    )

    def __init__(self, *, tiles: Iterable[TilesRow]) -> None:
        self.tiles = list(tiles)
        self.width = len(self.tiles[0]) if self.tiles else 0
        self.height = len(self.tiles)

    def get_tiles(self) -> Sequence[Sequence[Tile]]:
        return self.tiles

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def find_islands(self) -> FindIslandsResult:
        parser = IslandsParser(self)
        return parser.find_islands()

    @classmethod
    def read(cls, *, width: int, height: int) -> Self:
        return cls(tiles=cls._read_tiles(width=width, height=height))

    @classmethod
    def _read_tiles(cls, *, width: int, height: int) -> Iterable[TilesRow]:
        for y in range(height):
            tiles_row = sys.stdin.readline().strip()
            yield tiles_row[:width]


@dataclasses.dataclass(kw_only=True, slots=True)
class FindIslandsResult:
    count: int = 0
    max_size: int = 0


class IslandsParser:
    grid: Grid
    width: int
    height: int
    tiles: Sequence[Sequence[Tile]]

    positions_state: list[list[bool]]
    positions_queue: deque[Vector]

    count: int
    max_size: int
    size: int

    __slots__ = (
        'grid',
        'width',
        'height',
        'tiles',
        'positions_state',
        'positions_queue',
        'count',
        'max_size',
        'size',
    )

    def __init__(self, grid: Grid) -> None:
        self.grid = grid
        self.width = self.height = 0
        self.tiles = []

        self.positions_state = []
        self.positions_queue = deque()

        self.count = self.max_size = self.size = 0

    def find_islands(self) -> FindIslandsResult:
        self.width = self.grid.get_width()
        self.height = self.grid.get_height()
        self.tiles = self.grid.get_tiles()

        self.positions_state = [[False] * self.width for _y in range(self.height)]
        self.positions_queue = deque()

        self.count = self.max_size = self.size = 0

        for y in range(self.height):
            for x in range(self.width):
                if self.positions_state[y][x]:
                    continue

                if self.tiles[y][x] == TILE_LAND:
                    self._handle_island(x=x, y=y)

        return FindIslandsResult(count=self.count, max_size=self.max_size)

    def _handle_island(self, *, x: int, y: int) -> None:
        self.size = 0
        self._handle_tile(x=x, y=y)

        while self.positions_queue:
            x, y = self.positions_queue.popleft()

            for dx, dy in DIRECTIONS:
                neighbor_x = x + dx
                neighbor_y = y + dy

                if (
                        not (0 <= neighbor_x < self.width and 0 <= neighbor_y < self.height) or
                        self.positions_state[neighbor_y][neighbor_x]
                ):
                    continue

                if self.tiles[neighbor_y][neighbor_x] == TILE_LAND:
                    self._handle_tile(x=neighbor_x, y=neighbor_y)

        self.count += 1

        if self.max_size < self.size:
            self.max_size = self.size

    def _handle_tile(self, *, x: int, y: int) -> None:
        self.positions_state[y][x] = True
        self.positions_queue.append((x, y))
        self.size += 1


def main() -> None:
    height, width = map(int, input().split())
    grid = Grid.read(width=width, height=height)

    find_islands_result = grid.find_islands()
    print(find_islands_result.count, find_islands_result.max_size)


if __name__ == '__main__':
    main()
