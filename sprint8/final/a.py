# https://contest.yandex.ru/contest/26133/run-report/154076718/
#
# -- Принцип работы --
#
# --- Функция `unpack_chars()` ---
#
# Функция `unpack_chars()` выполняет распаковку строк, содержащих специальным образом закодированные
# повторения подстрок. Основная часть алгоритма распаковки реализована в классе `UnpackTool`. Для
# повышения эффективности, метод `UnpackTool.unpack_chars()` возвращает итератор символов, чтобы не
# обрабатывать без необходимости всю строку целиком.
#
# Метод `UnpackTool.unpack_chars()` последовательно считывает символы запакованной строки, перемещая
# целочисленный указатель на текущий символ до тех пор, пока строка не закончится. Для хранения
# вложенных циклов повторений подстрок используется стек.
#
# * Если очередной символ строки является цифрой, то мы запоминаем его значение как число повторений
#   следующей за ним запакованной подстроки и переходим к следующему символу.
# * Если был считан символ `[`, то мы инициализируем новый цикл повторения подстроки и добавляем его
#   в стек, сохраняя в объекте цикла начало подстроки и число ее повторений, после чего переходим к
#   следующему символу.
# * Если был считан символ `]`, то мы получаем из вершины стека внутренний цикл повторений и увеличиваем
#   его счетчик на единицу. Если цикл завершен, то мы удаляем его из стека. Иначе мы переводим указатель
#   на обрабатываемый символ в начало подстроки цикла.
# * Если очередной символ строки не является служебным, то мы просто возвращаем этот символ из генератора
#   и переходим к следующему.
#
# --- Функция `get_longest_common_prefix()` ---
#
# Функция `get_longest_common_prefix()` распаковывает строки и находит их наибольший общий префикс.
# Алгоритм определения наибольшего общего префикса реализован в классе `CommonPrefixTool`. Для повышения
# эффективности, метод `CommonPrefixTool._get_longest_common_prefix_chars()` возвращает итератор символов,
# чтобы не собирать их вручную в список перед объединением в строку.
#
# Нахождение наибольшего общего префикса в методе `CommonPrefixTool._get_longest_common_prefix_chars()`
# осуществляется путем посимвольного сравнения значений, которые возвращают итераторы, полученные в
# результате вызова функции `unpack_chars()` для запакованных строк. В каждой итерации цикла сравнения
# мы проверяем, совпадает ли очередной символ распакованной первой строки с соответствующими символами
# остальных строк. Если при сравнении символов было найдено расхождение, или же одна из строк неожиданно
# закончилась, то функция завершает работу. В противном случае генератор возвращает очередной символ.
#
# -- Доказательство корректности --
#
# В функции `unpack_chars()` выполнение вложенных циклов реализовано таким образом, что обработка
# строки не завершится с ошибкой даже при задании некорректной последовательности скобок. Поскольку
# максимально возможное число повторений цикла не превышает девяти, то все циклы рано или поздно будут
# завершены.
#
# Функция `get_longest_common_prefix()` фактически реализует классический алгоритм нахождения наибольшего
# общего префикса набора строк, основанный на посимвольном сравнении — за исключением того, что вместо
# строк используются итераторы символов.
#
# -- Временная сложность --
#
# Поскольку цикл сравнения строк выполняется до тех пор, пока не встретятся отличающиеся друг от друга
# символы, временную сложность алгоритма можно оценить как `O(n · min(|sᵢ|))`, где `n` — количество
# переданных строк, а `|sᵢ|` — длина строки номер `i` в распакованном виде.
#
# -- Пространственная сложность --
#
# В ходе своей работы алгоритм создает для каждой из строк объект класса `UnpackTool`, содержащий в
# одном из своих полей стек циклов повторений. Максимальное количество элементов этого стека зависит
# от исходных данных, но в среднем его можно оценить примерно как `O(log min(|sᵢ|))`, поскольку чем
# длиннее строка, тем больше вложенных циклов повторений символов она теоретически может включать, но
# при этом процедура распаковки будет ограничена минимальной длиной строки. Помимо этого, в методе
# `CommonPrefixTool.get_longest_common_prefix()` из символов создается строка, содержащая наибольший
# общий префикс длиной порядка `O(min(|sᵢ|))`. Таким образом, пространственная сложность алгоритма
# составляет `O(min(|sᵢ|) + n · log min(|sᵢ|))`.

from __future__ import annotations

import dataclasses
import sys
from collections.abc import Iterable, Iterator, Sequence, Mapping, Callable


def get_longest_common_prefix(strings: Sequence[str]) -> str:
    common_prefix_tool = CommonPrefixTool(strings)
    return common_prefix_tool.get_longest_common_prefix()


class CommonPrefixTool:
    strings: Sequence[str]

    __slots__ = (
        'strings',
    )

    def __init__(self, strings: Sequence[str]) -> None:
        self.strings = strings

    def get_longest_common_prefix(self) -> str:
        return ''.join(self._get_longest_common_prefix_chars())

    def _get_longest_common_prefix_chars(self) -> Iterable[str]:
        strings = self.strings
        strings_count = len(strings)

        if not strings_count:
            return

        char_iter_list = [unpack_chars(s) for s in strings]
        first_char_iter = char_iter_list[0]

        while True:
            try:
                char = next(first_char_iter)
            except StopIteration:
                return

            for i in range(1, strings_count):
                try:
                    other_char = next(char_iter_list[i])
                except StopIteration:
                    return

                if char != other_char:
                    return

            yield char


def unpack_chars(s: str) -> Iterator[str]:
    unpack_tool = UnpackTool(s)
    return unpack_tool.unpack_chars()


class Repetition:
    start_pos: int
    count: int
    index: int

    __slots__ = (
        'start_pos',
        'count',
        'index',
    )

    def __init__(self, *, start_pos: int, count: int) -> None:
        self.start_pos = start_pos
        self.count = count
        self.index = 0

    def get_start_pos(self) -> int:
        return self.start_pos

    def next(self) -> None:
        self.index += 1

    def has_finished(self) -> bool:
        return self.index >= self.count


class RepetitionsStack:
    repetitions: list[Repetition]

    __slots__ = (
        'repetitions',
    )

    def __init__(self) -> None:
        self.repetitions = []

    def push(self, repetition: Repetition) -> None:
        self.repetitions.append(repetition)

    def pop(self) -> None:
        if not self.repetitions:
            return

        self.repetitions.pop()

    def get_current(self) -> Repetition | None:
        if not self.repetitions:
            return None

        return self.repetitions[-1]


@dataclasses.dataclass(kw_only=True, slots=True)
class ParseTokenResult:
    new_pos: int


type TokenParser = Callable[[str, int], ParseTokenResult | None]


class UnpackTool:
    s: str
    repetitions_stack: RepetitionsStack
    repetition_count: int
    token_parsers: Mapping[str, TokenParser]

    __slots__ = (
        's',
        'repetitions_stack',
        'repetition_count',
        'token_parsers',
    )

    def __init__(self, s: str) -> None:
        self.s = s
        self.repetitions_stack = RepetitionsStack()
        self.repetition_count = 0
        self.token_parsers = self._get_token_parsers()

    def _get_token_parsers(self) -> Mapping[str, TokenParser]:
        token_parsers = {
            '[': self._parse_repetition_start,
            ']': self._parse_repetition_end,
        }

        _parse_repetition_count = self._parse_repetition_count
        token_parsers.update((str(digit), _parse_repetition_count) for digit in range(10))

        return token_parsers

    def unpack_chars(self) -> Iterator[str]:
        self.repetitions_stack = RepetitionsStack()
        self.repetition_count = 0

        s = self.s
        token_parsers = self.token_parsers
        s_length = len(s)
        pos = 0

        while pos < s_length:
            char = s[pos]
            token_parser = token_parsers.get(char)

            if token_parser is None:
                pos += 1
                yield char
                continue

            parse_token_result = token_parser(char, pos)

            if parse_token_result is None:
                pos += 1
                continue

            pos = parse_token_result.new_pos

    # noinspection PyUnusedLocal
    def _parse_repetition_count(self, char: str, pos: int) -> ParseTokenResult | None:
        try:
            self.repetition_count = int(char)
        except ValueError:
            return None

        return None

    # noinspection PyUnusedLocal
    def _parse_repetition_start(self, char: str, pos: int) -> ParseTokenResult | None:
        self.repetitions_stack.push(Repetition(
            start_pos=pos + 1,
            count=self.repetition_count,
        ))
        self.repetition_count = 0

        return None

    # noinspection PyUnusedLocal
    def _parse_repetition_end(self, char: str, pos: int) -> ParseTokenResult | None:
        current_repetition = self.repetitions_stack.get_current()

        if current_repetition is None:
            return None

        current_repetition.next()

        if current_repetition.has_finished():
            self.repetitions_stack.pop()
            return None

        start_pos = current_repetition.get_start_pos()

        return ParseTokenResult(
            new_pos=start_pos,
        )


def read_strings(count: int) -> Iterable[str]:
    for i in range(count):
        yield sys.stdin.readline().strip()


def main() -> None:
    strings_count = int(input().strip())
    strings = list(read_strings(strings_count))

    print(get_longest_common_prefix(strings))


if __name__ == '__main__':
    main()
