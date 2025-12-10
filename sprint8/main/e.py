from __future__ import annotations

import operator
import sys
from collections.abc import Iterable

type Substring = tuple[str, int]


def insert_substrings(s: str, t_it: Iterable[Substring]) -> Iterable[str]:
    t_list = list(t_it)
    t_list.sort(key=operator.itemgetter(1))

    i = 0

    for t in t_list:
        t_s, t_pos = t
        s_part = s[i:t_pos]

        if s_part:
            yield s_part

        if t_s:
            yield t_s

        i = t_pos

    s_part = s[i:]

    if s_part:
        yield s_part


def read_substrings(count: int) -> Iterable[Substring]:
    for i in range(count):
        values_list = sys.stdin.readline().rsplit(maxsplit=1)
        yield values_list[0], int(values_list[1])


def main() -> None:
    s = sys.stdin.readline().strip()
    t_count = int(input().strip())
    t_it = read_substrings(t_count)

    print(*insert_substrings(s, t_it), sep='')


if __name__ == '__main__':
    main()
