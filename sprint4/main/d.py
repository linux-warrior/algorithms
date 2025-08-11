from __future__ import annotations


def get_polynomial_hash(s: str, *, a: int, m: int) -> int:
    result = 0

    for char in s:
        result = (result * a + ord(char)) % m

    return result


def main() -> None:
    a = int(input().strip())
    m = int(input().strip())
    s = input().strip()

    polynomial_hash = get_polynomial_hash(s, a=a, m=m)
    print(polynomial_hash)


if __name__ == '__main__':
    main()
