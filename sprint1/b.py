from __future__ import annotations


def check_parity(*, a: int, b: int, c: int) -> bool:
    is_first_even = (a & 1) == 0

    for value in (b, c):
        is_value_even = (value & 1) == 0

        if is_value_even != is_first_even:
            return False

    return True


def main() -> None:
    a, b, c = map(int, input().strip().split())
    result = check_parity(a=a, b=b, c=c)
    print('WIN' if result else 'FAIL')


if __name__ == '__main__':
    main()
