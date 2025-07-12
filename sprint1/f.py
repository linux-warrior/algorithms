from __future__ import annotations


def is_palindrome(line: str) -> bool:
    i_start = 0
    i_end = len(line) - 1

    while i_start < i_end:
        char_start = line[i_start]

        if not char_start.isalnum():
            i_start += 1
            continue

        char_end = line[i_end]

        if not char_end.isalnum():
            i_end -= 1
            continue

        if char_start.lower() != char_end.lower():
            return False

        i_start += 1
        i_end -= 1

    return True


def main() -> None:
    line = input().strip()
    print(is_palindrome(line))


if __name__ == '__main__':
    main()
