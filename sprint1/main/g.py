from __future__ import annotations


def to_binary(value: int) -> str:
    result: list[int] = []

    while value != 0:
        result.append(value & 1)
        value >>= 1

    if not result:
        result.append(0)

    return ''.join(map(str, reversed(result)))


def main() -> None:
    value = int(input().strip())
    print(to_binary(value))


if __name__ == '__main__':
    main()
