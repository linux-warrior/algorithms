from __future__ import annotations

import sys


def is_subsequence(s: str, t: str) -> bool:
    if not s:
        return True

    if len(s) > len(t):
        return False

    i = j = 0

    while True:
        if s[i] == t[j]:
            i += 1

            if i == len(s):
                return True

        j += 1

        if j == len(t):
            return False


def main() -> None:
    s = sys.stdin.readline().strip()
    t = sys.stdin.readline().strip()
    print(is_subsequence(s, t))


if __name__ == '__main__':
    main()
