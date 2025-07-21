from __future__ import annotations


def fibonacci_recursive(n: int) -> int:
    if n < 2:
        return 1

    return fibonacci_recursive(n - 2) + fibonacci_recursive(n - 1)


def main() -> None:
    n = int(input().strip())
    print(fibonacci_recursive(n))


if __name__ == '__main__':
    main()
