import os

import dotenv

dotenv.load_dotenv()

_store: dict[str, str | None] = {
    "MONGO_URI": os.getenv("MONGO_URI"),
    "JWT_HASH": os.getenv("JWT_HASH"),
    "BCRYPT_HASH": os.getenv("BCRYPT_HASH"),
    "EXPIRTY_MINUTES": os.getenv("EXPIRTY_MINUTES"),
    "PORT": os.getenv("PORT"),
    "DICTIONARY_URI": os.getenv("DICTIONARY_URI"),
}


def get_env(key: str) -> str | None:
    """
    Retrieves the value of an environment variable by key.
    Args:
        key: The key of the environment variable to retrieve.

    Returns: The value of the environment variable, or None if not found.
    """
    return _store[key]
