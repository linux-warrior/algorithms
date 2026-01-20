# https://contest.yandex.ru/contest/24414/run-report/155573748/
#
# -- Принцип работы --
#
# Класс `HashTable` реализует хеш-таблицу, в которой для разрешения коллизий применяется метод цепочек.
# В зависимости от значения хеш-функции для ключа, добавляемый в хеш-таблицу элемент помещается в одну
# из существующих корзин. Количество корзин фиксировано в течение всего периода жизни хеш-таблицы,
# поскольку рехеширование элементов не поддерживается.
#
# Для хранения элементов в корзине используются питоновский список. Если добавляемого элемента с
# некоторым значением ключа не существует, то он сохраняется в конец списка, а если элемент с таким
# ключом в списке уже есть, то происходит обновление его значения. При получении элемента по ключу и
# при его удалении выполняется цикл по элементам списка, пока нужный элемент не будет найден.
#
# -- Доказательство корректности --
#
# Поскольку при добавлении, получении и удалении элемента с некоторым значением ключа каждый раз
# выполняется обращение к одной и той же корзине хеш-таблицы, то добавленный элемент всегда может
# быть позднее найден по его ключу.
#
# -- Временная сложность --
#
# Временная сложность добавления элемента в хеш-таблицу соответствует временной сложности добавления
# элемента в конец списка корзины и в среднем составляет `O(1)`. Поскольку при получении по ключу и
# при удалении элемента список корзины просматривается в цикле, то временная сложность этих операций
# в среднем составляет `O(1 + α)`, где `α` — коэффициент заполнения хеш-таблицы.
#
# -- Пространственная сложность --
#
# Пространственная сложность хеш-таблицы составляет `O(n)`, где `n` — число элементов таблицы.

from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence, Callable


class BucketNode:
    key: int
    value: int

    def __init__(self, key: int, value: int) -> None:
        self.key = key
        self.value = value


class BucketContainer:
    nodes: list[BucketNode]

    def __init__(self) -> None:
        self.nodes = []

    def __iter__(self) -> Iterator[BucketNode]:
        yield from self.nodes

    def find_node(self, key: int) -> BucketNode | None:
        for bucket_node in self:
            if bucket_node.key == key:
                return bucket_node

        return None

    def create_node(self, key: int, value: int) -> BucketNode:
        bucket_node = BucketNode(key, value)
        self.nodes.append(bucket_node)
        return bucket_node

    def delete_node(self, bucket_node: BucketNode) -> None:
        self.nodes.remove(bucket_node)


class Bucket:
    container: BucketContainer

    def __init__(self) -> None:
        self.container = BucketContainer()

    def get(self, key: int) -> int | None:
        bucket_node = self.container.find_node(key)

        if bucket_node is None:
            return None

        return bucket_node.value

    def put(self, key: int, value: int) -> None:
        bucket_node = self.container.find_node(key)

        if bucket_node is None:
            self.container.create_node(key, value)
            return

        bucket_node.value = value

    def delete(self, key: int) -> int | None:
        bucket_node = self.container.find_node(key)

        if bucket_node is None:
            return None

        value = bucket_node.value
        self.container.delete_node(bucket_node)
        return value


class HashTable:
    capacity: int
    buckets: Sequence[Bucket]

    def __init__(self, *, capacity: int) -> None:
        self.capacity = capacity
        self.buckets = [Bucket() for _i in range(capacity)]

    def _get_bucket(self, key: int) -> Bucket:
        return self.buckets[hash(key) % self.capacity]

    def get(self, key: int) -> int | None:
        bucket = self._get_bucket(key)
        return bucket.get(key)

    def put(self, key: int, value: int) -> None:
        bucket = self._get_bucket(key)
        bucket.put(key, value)

    def delete(self, key: int) -> int | None:
        bucket = self._get_bucket(key)
        return bucket.delete(key)


type HashTableCommandArgs = Sequence[int]
type HashTableCommandParser = Callable[[HashTableCommandArgs], str | None]


class HashTableCommandsExecutor:
    hash_table: HashTable
    command_parsers: Iterable[tuple[str, HashTableCommandParser]]

    def __init__(self, hash_table: HashTable) -> None:
        self.hash_table = hash_table
        self.command_parsers = self.get_command_parsers()

    def get_command_parsers(self) -> Iterable[tuple[str, HashTableCommandParser]]:
        return [
            ('get', self._parse_get),
            ('put', self._parse_put),
            ('delete', self._parse_delete),
        ]

    def execute(self, command_str: str) -> str | None:
        for command_name, command_parser in self.command_parsers:
            command_prefix = command_name + ' '

            if command_str.startswith(command_prefix):
                command_args = list(map(int, command_str.removeprefix(command_prefix).split()))
                return command_parser(command_args)

        return None

    def _parse_get(self, command_args: HashTableCommandArgs) -> str:
        value = self.hash_table.get(command_args[0])
        return str(value)

    def _parse_put(self, command_args: HashTableCommandArgs) -> None:
        self.hash_table.put(command_args[0], command_args[1])

    def _parse_delete(self, command_args: HashTableCommandArgs) -> str:
        value = self.hash_table.delete(command_args[0])
        return str(value)


def main() -> None:
    commands_count = int(input().strip())

    hash_table = HashTable(capacity=10000)
    commands_executor = HashTableCommandsExecutor(hash_table)

    for i in range(commands_count):
        command_str = input().strip()
        result = commands_executor.execute(command_str)

        if result is not None:
            print(result)


if __name__ == '__main__':
    main()
