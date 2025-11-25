from __future__ import annotations

from collections.abc import Iterable

type Time = tuple[int, int]
type Event = tuple[Time, Time]


def create_schedule(events: Iterable[Event]) -> Iterable[Event]:
    events_list = list(events)
    events_list.sort(key=lambda _event: (_event[1], _event[0]))
    previous_end_time: Time = (0, 0)

    for event in events_list:
        start_time, end_time = event

        if start_time >= previous_end_time:
            yield event
            previous_end_time = end_time


def read_events(count: int) -> Iterable[Event]:
    for i in range(count):
        start_time, end_time = map(parse_time, input().split())
        yield start_time, end_time


def parse_time(time_str: str) -> Time:
    values_list = list(map(int, time_str.strip().split('.')[:2]))

    if len(values_list) < 2:
        values_list.append(0)

    return values_list[0], values_list[1]


def render_time(time: Time) -> str:
    return f'{time[0]}.{time[1]}' if time[1] else str(time[0])


def main() -> None:
    events_count = int(input().strip())
    events = read_events(events_count)

    schedule = list(create_schedule(events))
    print(len(schedule))

    for start_time, end_time in schedule:
        print(*(render_time(time) for time in (start_time, end_time)))


if __name__ == '__main__':
    main()
