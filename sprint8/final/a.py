# https://contest.yandex.ru/contest/26133/run-report/154614832/
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
# Функция `get_longest_common_prefix()` последовательно распаковывает строки, получая итераторы
# символов из функции `unpack_chars()`, и находит их наибольший общий префикс, посимвольно сравнивая
# каждую распакованную строку с первой. По результатам сравнения очередной пары строк обновляется
# значение целочисленного указателя на конец общего префикса подмножества строк, обработанного на
# текущий момент. Если после проверки очередной строки окажется, что текущий наибольший общий префикс
# пустой, то функция прекращает дальнейшую распаковку строк и завершает работу.
#
# -- Доказательство корректности --
#
# В функции `unpack_chars()` выполнение вложенных циклов реализовано таким образом, что обработка
# строки не завершится с ошибкой даже при задании некорректной последовательности скобок. Поскольку
# максимально возможное число повторений цикла не превышает девяти, то все циклы рано или поздно будут
# завершены.
#
# Поскольку операция нахождения наибольшего общего префикса ассоциативна, то, распаковывая и сравнивая
# строки попарно, функция `get_longest_common_prefix()` найдет наибольший общий префикс всех переданных
# в нее строк.
#
# -- Временная сложность --
#
# Если наибольший общий префикс не является пустым, то функция `get_longest_common_prefix()` будет
# распаковывать каждую последующую переданную в нее строку до того момента, пока при ее сравнении с
# первой строкой не встретятся отличающиеся друг от друга символы. Поэтому временную сложность алгоритма
# можно оценить как `O(Σ(min(k₁|s₁|, kᵢ|sᵢ|)))`, где `|sᵢ|` — длина строки `i`, а `kᵢ` — коэффициент
# сжатия строки `i`, зависящий от количества повторений, которые содержатся в строке.

# -- Пространственная сложность --
#
# В ходе своей работы функция `get_longest_common_prefix()` сначала сохраняет в виде списка символов
# найденный наибольший общий префикс между первой и второй строкой, после чего она последовательно
# распаковывает оставшиеся строки, обновляя значение указателя на конец наибольшего общего префикса.
# Поэтому пространственную сложность алгоритма можно оценить как `O(min(k₁|s₁|, k₂|s₂|))`.

from __future__ import annotations

import dataclasses
import itertools
import sys
from collections.abc import Iterable, Iterator, Mapping, Callable


def get_longest_common_prefix(strings: Iterable[str]) -> str:
    strings_iter = iter(strings)

    try:
        packed_first_str = next(strings_iter)
    except StopIteration:
        return ''

    first_chars_iter = unpack_chars(packed_first_str)
    first_chars_list: list[str] = []
    end_pos: int | None = None

    for packed_other_str in strings_iter:
        other_chars_iter = unpack_chars(packed_other_str)
        pos = 0

        while True:
            if end_pos is None:
                try:
                    char = next(first_chars_iter)
                except StopIteration:
                    break

                first_chars_list.append(char)

            else:
                if pos == end_pos:
                    break

                char = first_chars_list[pos]

            try:
                other_char = next(other_chars_iter)
            except StopIteration:
                break

            if char != other_char:
                break

            pos += 1

        end_pos = pos

        if not end_pos:
            break

    chars_iter: Iterable[str] = (
        first_chars_iter if end_pos is None else itertools.islice(first_chars_list, end_pos)
    )

    return ''.join(chars_iter)


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
        token_parsers: dict[str, TokenParser] = {
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
    strings = read_strings(strings_count)

    print(get_longest_common_prefix(strings))


if __name__ == '__main__':
    main()
