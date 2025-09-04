from __future__ import annotations


def binomial_coeff(n: int, k: int) -> int:
    if k > n - k:
        return binomial_coeff(n, n - k)

    result = 1

    for i in range(k):
        result = result * (n - i) // (i + 1)

    return result


def get_unique_bst_count(n: int) -> int:
    return binomial_coeff(2 * n, n) // (n + 1)


def main() -> None:
    nodes_count = int(input().strip())
    unique_bst_count = get_unique_bst_count(nodes_count)
    print(unique_bst_count)


if __name__ == '__main__':
    main()
