# https://contest.yandex.ru/contest/24414/run-report/141654688/
#
# -- Принцип работы --
#
# Для хранения поискового индекса в классе `SearchIndex` используется питоновский словарь, ключами
# элементов которого служат слова добавляемых документов. Значениями элементов в свою очередь
# выступают словари, сопоставляющие порядковый номер документа, содержащего данное слово, и число
# вхождений слова в этот документ (релевантность). При добавлении в индекс документы разделяются
# на отдельные слова и сохраняются в указанный словарь.
#
# Во время поиска переданный запрос аналогичным образом разбивается на уникальные слова, после чего
# для этих слов в цикле формируется словарь результатов, сопоставляющий порядковые номера документов
# и значения их релевантности. Релевантность документа определяется как сумма значений релевантности
# всех слов из поискового запроса, которые содержит документ. После обработки всех слов запроса функция
# поиска возвращает требуемое число самых релевантных результатов (по умолчанию 5).
#
# -- Доказательство корректности --
#
# Поскольку поисковый индекс содержит информацию о релевантности всех слов для каждого из добавленных
# документов, то эти данные позволяют выполнить поиск любой фразы.
#
# -- Временная сложность --
#
# Временная сложность индексирования документов составляет `O(documents_count · document_words_count)`,
# где `documents_count` — общее число документов, а `document_words_count` — среднее количество слов в
# документе. Поскольку при поиске выполняются два вложенных цикла по словам запроса и проиндексированным
# документам, то временная сложность обработки поискового запроса составляет `O(query_words_count ·
# documents_count)`, где `query_words_count` — количество уникальных слов в запросе.
#
# -- Пространственная сложность --
#
# Пространственная сложность индексирования документов определяется размером памяти, занимаемой поисковым
# индексом, и составляет `O(documents_count · document_words_count)`. Так как во время поиска в памяти
# формируется словарь, сопоставляющий документы и их релевантность, то пространственная сложность поиска
# составляет `O(documents_count)`.

from __future__ import annotations

import heapq
import sys
from collections.abc import Iterable


class SearchIndex:
    index: dict[str, dict[int, int]]
    next_document_id: int

    def __init__(self) -> None:
        self.index = {}
        self.next_document_id = 1

    def add_documents(self, *, documents: Iterable[str]) -> None:
        for document in documents:
            self.add_document(document=document)

    def add_document(self, *, document: str) -> None:
        document_id = self.next_document_id
        self.next_document_id += 1

        for word in document.split():
            word_occurrences = self.index.setdefault(word, {})
            word_occurrences.setdefault(document_id, 0)
            word_occurrences[document_id] += 1

    def search(self, *, query: str, count: int = 5) -> Iterable[int]:
        words_set = set(query.split())
        search_results: dict[int, int] = {}

        for word in words_set:
            word_occurrences = self.index.get(word)

            if word_occurrences is None:
                continue

            for document_id, relevance in word_occurrences.items():
                search_results.setdefault(document_id, 0)
                search_results[document_id] += relevance

        most_relevant_results = heapq.nlargest(
            count,
            search_results.items(),
            key=lambda item: (item[1], -item[0]),
        )

        return [item[0] for item in most_relevant_results]


def read_strings(count: int) -> Iterable[str]:
    for i in range(count):
        yield sys.stdin.readline().strip()


def main() -> None:
    documents_count = int(input().strip())
    documents = list(read_strings(documents_count))
    queries_count = int(input().strip())
    queries = list(read_strings(queries_count))

    search_index = SearchIndex()

    for document in documents:
        search_index.add_document(document=document)

    for query in queries:
        documents_ids = search_index.search(query=query)
        print(*documents_ids)


if __name__ == '__main__':
    main()
