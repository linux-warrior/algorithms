from __future__ import annotations

import math
from collections.abc import Sequence


def factorize(value: int) -> Sequence[int]:
    if value < 2:
        return []

    result: list[int] = []
    value_sqrt = int(math.sqrt(value))
    i = 2

    while True:
        if i > value_sqrt:
            if value > 1:
                result.append(value)
            break

        if value % i:
            i += 1
            continue

        result.append(i)
        value //= i

    return result


def main() -> None:
    value = int(input().strip())
    result = factorize(value)
    print(' '.join(map(str, result)))


if __name__ == '__main__':
    main()
