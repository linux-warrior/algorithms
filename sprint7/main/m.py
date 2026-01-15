from __future__ import annotations

from collections.abc import Iterable, Sequence

type KnapsackItem = tuple[int, int]


def create_knapsack(items: Iterable[KnapsackItem], *, capacity: int) -> Sequence[int]:
    knapsack_values = [0] * (capacity + 1)
    selected_items: list[list[int]] = [[] for _total_weight in range(capacity + 1)]

    for i, item in enumerate(items):
        item_weight, item_value = item

        for total_weight in range(capacity, item_weight - 1, -1):
            new_total_value = knapsack_values[total_weight - item_weight] + item_value

            if new_total_value <= knapsack_values[total_weight]:
                continue

            knapsack_values[total_weight] = new_total_value
            selected_items[total_weight] = [*selected_items[total_weight - item_weight], i]

    return selected_items[-1]


def read_knapsack_items(count: int) -> Iterable[KnapsackItem]:
    for i in range(count):
        item_weight, item_value = map(int, input().split())
        yield item_weight, item_value


def main() -> None:
    items_count, capacity = map(int, input().split())
    items = read_knapsack_items(items_count)

    knapsack = create_knapsack(items, capacity=capacity)
    print(len(knapsack))
    print(*map(lambda i: i + 1, knapsack))


if __name__ == '__main__':
    main()
