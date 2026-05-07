from datetime import datetime
from uuid import uuid4


def generate_id() -> str:
    """
    utility function to generate a unique identifier using UUID4.

    Returns: A string representation of a UUID4, which is a universally unique identifier to avoid conflicts.

    """
    return str(uuid4())


def current_time() -> datetime:
    """
    utility function to get the current date and time.

    Returns: A datetime object representing the current date and time when the function is called.

    """
    return datetime.now()
