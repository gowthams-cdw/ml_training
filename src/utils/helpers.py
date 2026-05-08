from uuid import uuid4

def gen_uuid() -> str:
    """
    Generates a unique UUID string.
    Returns: A unique UUID string.
    """
    return str(uuid4())
