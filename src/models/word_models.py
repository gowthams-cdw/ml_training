from pydantic import BaseModel


class Word(BaseModel):
    """
    A model representing a word entry.
    Attributes:
        id: The unique identifier for the word.
        word: The word itself.
        meaning: The meaning of the word.
    """
    id: str
    word: str
    meaning: str


class WordCreate(BaseModel):
    """
    A model representing the data required to create a new word entry.
    Attributes:
        word: The word itself.
        meaning: The meaning of the word.
    """
    word: str
    word_meaning: str

class SpecificWordRequest(BaseModel):
    """
    A model representing the data required to request a specific word entry.
    Attributes:
        word_id: The unique identifier for the word to be requested.
    """
    word_id: str
