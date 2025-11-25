from __future__ import annotations


def fibonacci_mod_dynamic(n: int, *, module: int) -> int:
    if module < 2:
        return 0

    if n < 2:
        return 1

    elements = [0] * (n + 1)
    elements[0] = elements[1] = 1

    for i in range(2, n + 1):
        elements[i] = (elements[i - 1] + elements[i - 2]) % module

    return elements[n]


def main() -> None:
    n = int(input().strip())
    print(fibonacci_mod_dynamic(n, module=10 ** 9 + 7))


if __name__ == '__main__':
    main()
