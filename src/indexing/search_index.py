from collections import defaultdict

class SearchIndex:
    def __init__(self) -> None:
        self._index: defaultdict[str, set[str]] = defaultdict(set)

    def index_file(self, file_id: str, content: str):
        cleanedWords = content.lower().split()

        for word in cleanedWords:
            self._index[word].add(file_id)

    def search(self, word: str) -> set[str]:
        return self._index[word.lower()]

    def remove(self, file_id) -> None:
        for word, values in self._index.items():
            if file_id in values:
                self._index[word].remove(file_id)
