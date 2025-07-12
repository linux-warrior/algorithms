from __future__ import annotations


def get_extra_letter(a: str, b: str) -> str:
    if len(b) != len(a) + 1:
        return ''

    code_points_diff = 0

    for b_char in b:
        code_points_diff += ord(b_char)

    for a_char in a:
        code_points_diff -= ord(a_char)

    return chr(code_points_diff)


def main() -> None:
    a, b = [input().strip() for _i in range(2)]
    print(get_extra_letter(a, b))


if __name__ == '__main__':
    main()
