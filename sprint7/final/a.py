# https://contest.yandex.ru/contest/25597/run-report/152748986/
#
# -- Принцип работы --
#
# Для определения расстояния Левенштейна между двумя строками, в функции `get_levenstein_distance()`
# реализован модифицированный алгоритм Вагнера — Фишера. Вместо целочисленной матрицы, в которую
# классический алгоритм записывает вычисленные расстояния между префиксами исходных строк, для экономии
# памяти мы будем использовать только текущую обрабатываемую строку этой матрицы и два элемента из ее
# предыдущей строки. Этих данных будет достаточно, чтобы в цикле рассчитать расстояние между очередной
# парой префиксов.
#
# -- Доказательство корректности --
#
# Доказательство корректности алгоритма Вагнера — Фишера можно найти в открытых источниках:
# https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm#Proof_of_correctness.
#
# -- Временная сложность --
#
# Поскольку в ходе работы функции вычисляются расстояния между всеми возможными парами префиксов
# исходных строк, временная сложность алгоритма составляет `O(|a| · |b|)`, где `|a|` и `|b|` —
# длины строк, переданных в качестве параметров.
#
# -- Пространственная сложность --
#
# Поскольку промежуточные результаты вычислений сохраняются в одномерный массив, длина которого на
# единицу больше длины самой короткой из исходных строк, пространственная сложность алгоритма составляет
# `O(min(|a|, |b|))`.

from __future__ import annotations

import sys


def get_levenstein_distance(a: str, b: str) -> int:
    a_length = len(a)
    b_length = len(b)

    if b_length > a_length:
        return get_levenstein_distance(b, a)

    distances = list(range(b_length + 1))

    for a_i in range(1, a_length + 1):
        distances_top_left = distances[0]
        distances[0] = a_i

        for b_i in range(1, b_length + 1):
            distances_top = distances[b_i]
            distances[b_i] = distances_top_left if a[a_i - 1] == b[b_i - 1] else min(
                distances[b_i - 1],
                distances_top_left,
                distances_top,
            ) + 1
            distances_top_left = distances_top

    return distances[b_length]


def main() -> None:
    a = sys.stdin.readline().strip()
    b = sys.stdin.readline().strip()

    print(get_levenstein_distance(a, b))


if __name__ == '__main__':
    main()
