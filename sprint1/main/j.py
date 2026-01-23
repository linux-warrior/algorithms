from __future__ import annotations

import math
from collections.abc import Iterable


def factorize(value: int) -> Iterable[int]:
    if value < 2:
        return

    value_sqrt = int(math.sqrt(value))
    i = 2

    while True:
        if i > value_sqrt:
            if value > 1:
                yield value

            break

        if value % i:
            i += 1
            continue

        yield i
        value //= i


def main() -> None:
    value = int(input().strip())

    print(*factorize(value))


if __name__ == '__main__':
    main()
