from __future__ import annotations

import sys


def can_translate(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False

    a_translation_map: dict[str, str] = {}
    b_translation_map: dict[str, str] = {}

    for i in range(len(a)):
        a_char = a[i]
        b_char = b[i]

        translated_a_char = a_translation_map.get(a_char)

        if translated_a_char is None:
            a_translation_map[a_char] = b_char
        elif translated_a_char != b_char:
            return False

        translated_b_char = b_translation_map.get(b_char)

        if translated_b_char is None:
            b_translation_map[b_char] = a_char
        elif translated_b_char != a_char:
            return False

    return True


def main() -> None:
    a = sys.stdin.readline().strip()
    b = sys.stdin.readline().strip()

    print('YES' if can_translate(a, b) else 'NO')


if __name__ == '__main__':
    main()
