from __future__ import annotations


def fibonacci_mod(n: int, k: int) -> int:
    if k < 1:
        return 0

    if n < 2:
        return 1

    elements = [1] * 2
    module: int = 10 ** k
    i = 2

    while True:
        element = (elements[0] + elements[1]) % module

        if i == n:
            return element

        elements[0] = elements[1]
        elements[1] = element
        i += 1


def main() -> None:
    n, k = map(int, input().strip().split())
    print(fibonacci_mod(n, k))


if __name__ == '__main__':
    main()
