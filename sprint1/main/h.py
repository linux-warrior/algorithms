from __future__ import annotations


def binary_sum(a: str, b: str) -> str:
    if len(b) > len(a):
        a, b = b, a

    result: list[int] = []
    a_i = len(a) - 1
    b_i = len(b) - 1
    carry = 0

    while a_i >= 0:
        a_digit = int(a[a_i])
        b_digit = int(b[b_i]) if b_i >= 0 else 0

        sum_part = a_digit + b_digit + carry
        sum_digit = sum_part & 1
        carry = sum_part >> 1
        result.append(sum_digit)

        a_i -= 1
        b_i -= 1

    if carry:
        result.append(carry)

    if not result:
        result.append(0)

    return ''.join(map(str, reversed(result)))


def main() -> None:
    a, b = [input().strip() for _i in range(2)]
    print(binary_sum(a, b))


if __name__ == '__main__':
    main()
