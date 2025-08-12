from __future__ import annotations

import sys


def get_polynomial_hash(string: str, *, a: int, m: int) -> int:
    result = 0

    for char in string:
        result = (result * a + ord(char)) % m

    return result


def main() -> None:
    a = int(input().strip())
    m = int(input().strip())
    string = sys.stdin.readline().strip()

    hash_value = get_polynomial_hash(string, a=a, m=m)
    print(hash_value)


if __name__ == '__main__':
    main()
