from __future__ import annotations

from collections.abc import Iterable

type Interval = tuple[int, int]


def merge_intervals(intervals: Iterable[Interval]) -> Iterable[Interval]:
    intervals_list = list(intervals)

    if not intervals_list:
        return

    intervals_list.sort()
    previous_left_endpoint, previous_right_endpoint = intervals_list[0]

    for i in range(1, len(intervals_list)):
        left_endpoint, right_endpoint = intervals_list[i]

        if left_endpoint <= previous_right_endpoint:
            previous_right_endpoint = max(right_endpoint, previous_right_endpoint)
            continue

        yield previous_left_endpoint, previous_right_endpoint

        previous_left_endpoint = left_endpoint
        previous_right_endpoint = right_endpoint

    yield previous_left_endpoint, previous_right_endpoint


def read_intervals(count: int) -> Iterable[Interval]:
    for i in range(count):
        left_endpoint, right_endpoint = map(int, input().strip().split())
        yield left_endpoint, right_endpoint


def main() -> None:
    intervals_count = int(input().strip())
    intervals = read_intervals(intervals_count)

    for left_endpoint, right_endpoint in merge_intervals(intervals):
        print(left_endpoint, right_endpoint)


if __name__ == '__main__':
    main()
