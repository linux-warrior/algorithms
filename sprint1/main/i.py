from __future__ import annotations


def is_power_of_4(value: int) -> bool:
    if value <= 0:
        return False

    while value > 1:
        if value & 3:
            return False

        value >>= 2

    return True


def main() -> None:
    value = int(input().strip())
    print(is_power_of_4(value))


if __name__ == '__main__':
    main()
