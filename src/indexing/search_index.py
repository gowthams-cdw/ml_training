from collections import defaultdict

class SearchIndex:
    """
    A simple search index that allows indexing files by their content and searching for files containing specific words.
    """
    def __init__(self) -> None:
        self._index: defaultdict[str, set[str]] = defaultdict(set)

    def index_file(self, file_id: str, content: str):
        """
        indexes a file by its content. Each word in the content is associated with the file_id in the index.

        Args:
            file_id: The identifier of the file to be indexed.
            content: The content of the file to be indexed.
        """
        cleanedWords = content.lower().split()

        for word in cleanedWords:
            self._index[word].add(file_id)

    def search(self, word: str) -> set[str]:
        """
        Searches for files containing the specified word and returns a set of file identifiers.

        Args:
            word: The word to search for in the indexed files.

        Returns: A set of file identifiers that contain the specified word.

        """
        return self._index[word.lower()]

    def remove(self, file_id: str) -> None:
        """
        Removes a file from the index by its identifier. This method iterates through the index and removes the file_id from any word associations.

        Args:
            file_id: The identifier of the file to be removed from the index.
        """
        for word, values in self._index.items():
            if file_id in values:
                self._index[word].remove(file_id)
