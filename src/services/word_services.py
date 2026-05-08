from typing import Optional

import requests

from config.env import get_env
from services.db_services import get_collection, get_db
from utils.helpers import gen_uuid


def get_word_collection():
    """
    Retrieves the word collection from the database.
    Returns: The word collection instance.
    """
    db = get_db("word_learner")
    return get_collection(db, "words")


async def get_word(word: str) -> Optional[dict]:
    """
    Retrieves a word document from the database by word.
    Args:
        word: The word to retrieve.

    Returns: The word document as a dictionary if found, otherwise None.
    """
    word_collection = get_word_collection()

    return await word_collection.find_one({"word": word})


async def get_word_id(word_id: str) -> Optional[dict]:
    """
    Retrieves a word document from the database by ID.
    Args:
        word_id: The unique identifier of the word to retrieve.

    Returns: The word document as a dictionary if found, otherwise None.
    """
    word_collection = get_word_collection()

    return await word_collection.find_one({"id": word_id})


async def create_word(word: str) -> str:
    """
    Creates a new word document in the database.
    Args:
        word: The word to create.

    Returns: The unique identifier of the created word.
    """
    word_collection = get_word_collection()

    word_id = gen_uuid()

    DICTIONARY_URI=get_env("DICTIONARY_URI")
    meaning = "Missing dictionary meaning."

    if DICTIONARY_URI:
        response = requests.get(f"{DICTIONARY_URI}/{word}")
        word_meaning = response.json()

        if isinstance(word_meaning, list) and len(word_meaning) > 0:
            meanings = word_meaning[0].get("meanings", [])

            if meanings:
                definitions = meanings[0].get("definitions", [])

                if definitions:
                    meaning = definitions[0].get(
                        "definition", "Missing dictionary meaning."
                    )

    await word_collection.insert_one(
        {
            "id": word_id,
            "word": word,
            "meaning": meaning,
        }
    )

    return word_id
