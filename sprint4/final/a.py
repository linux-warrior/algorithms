from __future__ import annotations

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

        results_items = list(search_results.items())
        results_items.sort(key=lambda item: (-item[1], item[0]))

        return [item[0] for item in results_items][:count]


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
