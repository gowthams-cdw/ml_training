from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

_client: AsyncMongoClient | None = None


def connect_db(mongo_uri: str) -> AsyncMongoClient:
    """
    Establishes a connection to the MongoDB database using the provided URI.
    Args:
        mongo_uri: The MongoDB connection URI.
    Returns: The connected AsyncMongoClient instance.
    """
    global _client

    if not _client:
        _client = AsyncMongoClient(mongo_uri)

    return _client


def get_db(db_name: str) -> AsyncDatabase:
    """
    Retrieves a specific database from the connected MongoDB client.
    Args:
        db_name: The name of the database to retrieve.

    Returns:  The requested AsyncDatabase instance.

    Raises :
        Exception: If the database connection has not been established.
    """
    global _client

    if not _client:
        raise Exception("DB not connected.")

    return _client[db_name]


def get_collection(db: AsyncDatabase, collection_name: str) -> AsyncCollection:
    """
    Retrieves a specific collection from the given database.
    Args:
        db: The AsyncDatabase instance.
        collection_name: The name of the collection to retrieve.

    Returns: The requested AsyncCollection instance.
    """
    return db[collection_name]
