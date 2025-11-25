from __future__ import annotations

import operator
from collections.abc import Iterable

type SandHeap = tuple[int, int]


def get_max_total_price(sand_heaps: Iterable[SandHeap], *, capacity: int) -> int:
    sand_heaps_list = list(sand_heaps)
    sand_heaps_list.sort(key=operator.itemgetter(0), reverse=True)

    result = 0

    for sand_price, heap_weight in sand_heaps_list:
        if capacity < 0:
            break

        sand_weight = heap_weight if heap_weight < capacity else capacity
        capacity -= sand_weight
        result += sand_price * sand_weight

    return result


def read_sand_heaps(count: int) -> Iterable[SandHeap]:
    for i in range(count):
        sand_price, heap_weight = map(int, input().split())
        yield sand_price, heap_weight


def main() -> None:
    capacity = int(input().strip())
    sand_heaps_count = int(input().strip())
    sand_heaps = read_sand_heaps(sand_heaps_count)

    total_price = get_max_total_price(sand_heaps, capacity=capacity)
    print(total_price)


if __name__ == '__main__':
    main()
