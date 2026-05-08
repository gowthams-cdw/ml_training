from typing import Optional

from fastapi import HTTPException

from services.db_services import get_collection, get_db


def get_user_collection():
    """
    Retrieves the user collection from the database.
    Returns: The user collection instance.
    """
    db = get_db("word_learner")
    return get_collection(db, "users")


async def get_user_by_username(username: str) -> Optional[dict]:
    """
    Retrieves a user document from the database by username.
    Args:
        username: The username of the user to retrieve.

    Returns: The user document as a dictionary if found, otherwise None.
    """
    user_collection = get_user_collection()
    return await user_collection.find_one({"username": username})


async def create_user(username: str, password: str):
    """
    Creates a new user document in the database with the provided username and password.
    Args:
        username: The username of the user to create.
        password: The password of the user to create.
    """
    user_collection = get_user_collection()

    await user_collection.insert_one({"username": username, "password": password})


async def update_user(username: str, data: dict):
    """
    Updates an existing user document in the database with the provided data.
    Args:
        username: The username of the user to update.
        data: The data to update the user document with.

    Raises:
        HTTPException: If the user does not exist.
    """
    user_collection = get_user_collection()

    existing_user = await get_user_by_username(username)
    if not existing_user:
        raise HTTPException(404, "User not exists")
    await user_collection.find_one_and_update({"username": username}, {"$set": data})
