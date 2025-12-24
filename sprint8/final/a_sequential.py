# https://contest.yandex.ru/contest/26133/run-report/154297342/
#
# -- Принцип работы --
#
# --- Функция `unpack()` ---
#
# Функция `unpack()` осуществляет распаковку строк, содержащих специальным образом закодированные
# повторения подстрок. Функция обрабатывает в цикле все символы запакованной строки, выполняя
# определенную операцию в зависимости от класса очередного символа. Для хранения вложенных циклов
# повторений подстрок используется стек. В целях удобства вся строка целиком тоже считается однократным
# повторением своего содержимого, а в стек добавляется соответствующий элемент.
#
# * Если очередной символ строки — алфавитный, то мы добавляем этот символ в содержимое вершины стека.
# * Если очередной символ строки является цифрой, то мы запоминаем его значение как число повторений
#   следующей за ним запакованной подстроки.
# * Если был считан символ `[`, то мы инициализируем новый цикл повторения подстроки и добавляем его
#   в стек, сохраняя в элементе число повторений.
# * Если был считан символ `]`, то мы удаляем из стека внутренний цикл повторений и сохраняем его
#   содержимое, умноженное на количество повторений, в новую вершину стека.
#
# --- Функция `get_longest_common_prefix()` ---
#
# Функция `get_longest_common_prefix()` последовательно распаковывает строки и находит их наибольший
# общий префикс, посимвольно сравнивая каждую распакованную строку с первой. По результатам сравнения
# очередной пары строк обновляется значение целочисленного указателя на конец общего префикса
# подмножества строк, обработанного на текущий момент. Если после проверки очередной строки окажется,
# что текущий наибольший общий префикс пустой, то функция прекращает дальнейшую распаковку строк и
# завершает работу.
#
# -- Доказательство корректности --
#
# В функции `unpack()` выполнение вложенных циклов реализовано таким образом, что обработка строки
# не завершится с ошибкой даже при задании некорректной последовательности скобок. Поскольку максимально
# возможное число повторений цикла не превышает девяти, то все циклы рано или поздно будут завершены.
#
# Поскольку операция нахождения наибольшего общего префикса ассоциативна, то, распаковывая и сравнивая
# строки попарно, функция `get_longest_common_prefix()` найдет наибольший общий префикс всех переданных
# в нее строк.
#
# -- Временная сложность --
#
# Если наибольший общий префикс не является пустым, то функция `get_longest_common_prefix()` распакует
# все переданные в нее строки. Поэтому временную сложность алгоритма можно оценить как `O(Σ(kᵢ|sᵢ|))`,
# где `|sᵢ|` — длина строки `i`, а `kᵢ` — коэффициент сжатия строки `i`, зависящий от количества
# повторений, которые содержатся в строке.
#
# -- Пространственная сложность --
#
# В ходе своей работы функция `get_longest_common_prefix()` последовательно распаковывает переданные
# в нее строки и сохраняет результат распаковки, начиная со второй строки, в одну и ту же переменную.
# Поэтому пространственную сложность алгоритма можно оценить как `O(max(kᵢ|sᵢ|))`.

from __future__ import annotations

import sys
from collections.abc import Iterable


def get_longest_common_prefix(strings: Iterable[str]) -> str:
    strings_iter = iter(strings)

    try:
        packed_first_str = next(strings_iter)
    except StopIteration:
        return ''

    first_str = unpack(packed_first_str)
    end_pos = len(first_str)

    for packed_other_str in strings_iter:
        other_str = unpack(packed_other_str)
        end_pos = min(end_pos, len(other_str))
        pos = 0

        while pos < end_pos:
            if first_str[pos] != other_str[pos]:
                break

            pos += 1

        end_pos = pos

        if not end_pos:
            break

    return first_str[:end_pos]


type Repetition = tuple[int, list[str]]


def unpack(s: str) -> str:
    repetitions_stack: list[Repetition] = []
    current_repetition: Repetition = (1, [])
    repetitions_stack.append(current_repetition)
    repetition_count = 0

    for char in s:
        if char.isalpha():
            current_repetition[1].append(char)

        elif char.isdigit():
            repetition_count = int(char)

        elif char == '[':
            current_repetition = (repetition_count, [])
            repetitions_stack.append(current_repetition)
            repetition_count = 0

        elif char == ']':
            if len(repetitions_stack) < 2:
                continue

            repetitions_stack.pop()
            previous_repetition = current_repetition
            current_repetition = repetitions_stack[-1]
            current_repetition[1].extend(_render_repetition(previous_repetition))

    return ''.join(_render_repetition(current_repetition))


def _render_repetition(repetition: Repetition) -> Iterable[str]:
    content = ''.join(repetition[1])

    for i in range(repetition[0]):
        yield content


def read_strings(count: int) -> Iterable[str]:
    for i in range(count):
        yield sys.stdin.readline().strip()


def main() -> None:
    strings_count = int(input().strip())
    strings = read_strings(strings_count)

    print(get_longest_common_prefix(strings))


if __name__ == '__main__':
    main()
