from __future__ import annotations

import dataclasses
import sys
from collections.abc import Iterable, Sequence
from typing import Self

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


type FlowersCounts = list[int]


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
        self.flowers_counts = [0] * self.width
        self._fill_flowers_counts()

        return GridPath(flowers_count=self.flowers_counts[-1])

    def _fill_flowers_counts(self) -> None:
        self.flowers_counts[0] = int(self.tiles[-1][0])

        for x in range(1, self.width):
            self.flowers_counts[x] = self.flowers_counts[x - 1] + int(self.tiles[-1][x])

        for y in range(self.height - 2, -1, -1):
            self.flowers_counts[0] += int(self.tiles[y][0])

            for x in range(1, self.width):
                self.flowers_counts[x] = max(
                    self.flowers_counts[x - 1],
                    self.flowers_counts[x],
                ) + int(self.tiles[y][x])


def main() -> None:
    height, width = map(int, input().split())
    grid = Grid.read(width=width, height=height)

    best_path = grid.find_best_path()
    print(best_path.flowers_count)


if __name__ == '__main__':
    main()
