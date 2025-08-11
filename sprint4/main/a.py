from __future__ import annotations

from collections.abc import Iterable


def get_unique_names(names: Iterable[str]) -> Iterable[str]:
    names_dict: dict[str, bool] = {}

    for name in names:
        names_dict[name] = True

    return names_dict.keys()


def read_names(count: int) -> Iterable[str]:
    for i in range(count):
        yield input().strip()


def main() -> None:
    names_count = int(input().strip())
    names = read_names(names_count)

    for name in get_unique_names(names):
        print(name)


if __name__ == '__main__':
    main()
