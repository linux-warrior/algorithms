from __future__ import annotations

import dataclasses
import enum
import sys
from collections import deque
from collections.abc import Iterable, Sequence, Mapping
from typing import Self, ClassVar

type Vector = tuple[int, int]


class DirectionType(enum.StrEnum):
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'


DIRECTIONS: Mapping[DirectionType, Vector] = {
    DirectionType.LEFT: (-1, 0),
    DirectionType.RIGHT: (1, 0),
    DirectionType.UP: (0, -1),
    DirectionType.DOWN: (0, 1),
}

type Tile = str
type TilesRow = str

TILE_WATER = '.'
TILE_LAND = '#'


@dataclasses.dataclass(kw_only=True)
class FindIslandsResult:
    count: int = 0
    max_size: int = 0


class Grid:
    tiles: list[TilesRow]
    width: int
    height: int

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
        parser.parse()

        return FindIslandsResult(
            count=parser.get_count(),
            max_size=parser.get_max_size(),
        )

    @classmethod
    def read(cls, *, width: int, height: int) -> Self:
        return cls(tiles=cls._read_tiles(width=width, height=height))

    @classmethod
    def _read_tiles(cls, *, width: int, height: int) -> Iterable[TilesRow]:
        for y in range(height):
            tiles_row = sys.stdin.readline().strip()
            yield tiles_row[:width]


class IslandsParser:
    directions: ClassVar[Sequence[Vector]] = list(DIRECTIONS.values())

    grid: Grid
    width: int
    height: int
    tiles: Sequence[Sequence[Tile]]

    positions_state: list[list[bool]]
    positions_queue: deque[Vector]

    count: int
    max_size: int
    size: int

    def __init__(self, grid: Grid) -> None:
        self.grid = grid
        self.width = self.height = 0
        self.tiles = []

        self.positions_state = []
        self.positions_queue = deque()

        self.count = self.max_size = self.size = 0

    def get_count(self) -> int:
        return self.count

    def get_max_size(self) -> int:
        return self.max_size

    def parse(self) -> None:
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

    def _handle_island(self, *, x: int, y: int) -> None:
        self.size = 0
        self._handle_tile(x=x, y=y)

        while self.positions_queue:
            x, y = self.positions_queue.popleft()

            for dx, dy in self.directions:
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
