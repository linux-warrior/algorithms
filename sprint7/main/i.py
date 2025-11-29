from __future__ import annotations

import dataclasses
import enum
import sys
from collections.abc import Iterable, Sequence
from typing import Self

type Vector = tuple[int, int]


class DirectionType(enum.StrEnum):
    RIGHT = 'R'
    UP = 'U'


type Tile = str
type TilesRow = str


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

    def find_best_path(self) -> GridPath:
        path_finder = GridPathFinder(self)
        return path_finder.find_best_path()

    @classmethod
    def read(cls, *, width: int, height: int) -> Self:
        return cls(tiles=cls._read_tiles(width=width, height=height))

    @classmethod
    def _read_tiles(cls, *, width: int, height: int) -> Iterable[TilesRow]:
        for y in range(height):
            tiles_row = sys.stdin.readline().strip()
            yield tiles_row[:width]


@dataclasses.dataclass(kw_only=True)
class GridPath:
    flowers_count: int = 0
    directions: Sequence[DirectionType] = dataclasses.field(default_factory=list)


type FlowersCounts = list[list[int]]


class GridPathFinder:
    grid: Grid
    width: int
    height: int
    tiles: Sequence[Sequence[Tile]]
    flowers_counts: FlowersCounts

    def __init__(self, grid: Grid) -> None:
        self.grid = grid
        self.width = self.height = 0
        self.tiles = []
        self.flowers_counts = []

    def find_best_path(self) -> GridPath:
        self.width = self.grid.get_width()
        self.height = self.grid.get_height()

        if self.width < 1 or self.height < 1:
            return GridPath()

        self.tiles = self.grid.get_tiles()
        self.flowers_counts = self._create_flowers_counts()
        self._fill_flowers_counts()
        path_directions = self._restore_path_directions()

        return GridPath(
            flowers_count=self.flowers_counts[0][-1],
            directions=path_directions,
        )

    def _create_flowers_counts(self) -> FlowersCounts:
        flowers_counts: FlowersCounts = []

        for _y in range(self.height):
            flowers_counts_row = [0] * (self.width + 1)
            flowers_counts_row[0] = -1
            flowers_counts.append(flowers_counts_row)

        flowers_counts.append([-1] * (self.width + 1))

        for position in [(0, -1), (1, -1), (0, -2)]:
            flowers_counts[position[1]][position[0]] = 0

        return flowers_counts

    def _fill_flowers_counts(self) -> None:
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                self.flowers_counts[y][x + 1] = max(
                    self.flowers_counts[y][x],
                    self.flowers_counts[y + 1][x + 1],
                ) + int(self.tiles[y][x])

    def _restore_path_directions(self) -> Sequence[DirectionType]:
        path_directions: list[DirectionType] = []

        x = self.width - 1
        y = 0

        while x > 0 or y < self.height - 1:
            direction_type: DirectionType

            if self.flowers_counts[y + 1][x + 1] > self.flowers_counts[y][x]:
                direction_type = DirectionType.UP
                y += 1
            else:
                direction_type = DirectionType.RIGHT
                x -= 1

            path_directions.append(direction_type)

        path_directions.reverse()

        return path_directions


def main() -> None:
    height, width = map(int, input().split())
    grid = Grid.read(width=width, height=height)

    best_path = grid.find_best_path()
    print(best_path.flowers_count)
    print(''.join(best_path.directions))


if __name__ == '__main__':
    main()
