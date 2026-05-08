from fastapi import APIRouter, Depends, HTTPException

from models.user_models import LoginUser, UserCreate, UserWord, UserWordUpdate
from models.word_models import WordCreate
from services.user_services import create_user, get_user_by_username, update_user
from services.word_services import create_word, get_word, get_word_id
from utils.auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/create", status_code=201)
async def register_user(data: UserCreate):
    """
    Registers a new user.
    Args:
        data: The user creation data containing username and password.

    Returns: A success message upon successful user creation.

    Raises:
        HTTPException: If a user with the same username already exists.
    """
    existing_user = await get_user_by_username(data.username)

    if existing_user:
        raise HTTPException(409, "User already exists")

    await create_user(data.username, hash_password(data.password))
    return {"message": "User created successfully."}


@user_router.post("/login")
async def login_user(data: LoginUser):
    """
    Logs in an existing user.
    Args:
        data: The login data containing username and password.

    Returns: A JWT access token upon successful login.

    Raises:
        HTTPException: If the user does not exist or if the credentials are invalid.
    """
    existing_user = await get_user_by_username(data.username)

    if not existing_user:
        raise HTTPException(404, "User not exists")

    if not verify_password(data.password, existing_user["password"]):
        raise HTTPException(400, "Invalid credentials.")

    return create_access_token({"username": existing_user["username"]})


@user_router.post("/word", status_code=201)
async def add_word(
    body: WordCreate,
    current_user: str = Depends(decode_access_token),
):
    """
    Adds a new word to the current user's list.
    Args:
        body: The word creation data.
        current_user: The username of the current user.

    Returns: A success message upon successfully adding the word to the user's list.

    Raises:
        HTTPException: If the user does not exist or if there is an issue with adding the word.
    """
    existing_user = await get_user_by_username(current_user)

    if not existing_user:
        raise HTTPException(404, "User not exists")

    existing_word = await get_word(body.word)

    if not existing_word:
        await create_word(body.word)
        existing_word = await get_word(body.word)
    if not existing_word or "id" not in existing_word:
        raise HTTPException(500, "Something went wrong")

    new_word = UserWord(
        word_id=str(existing_word.get("id")),
        user_definition=body.word_meaning,
        mastered=False,
    )
    words = existing_user.get("words", []).copy()
    words.append(new_word.model_dump())

    await update_user(current_user, {"words": words})
    return {
        "message": f"Word '{body.word}' with {existing_word.get('id')} as id is added to user '{current_user}' successfully."
    }


@user_router.get("/word", status_code=200)
async def get_all_words(
    mastered: bool | None = None, current_user: str = Depends(decode_access_token)
):
    """
    Retrieves all words for the current user, optionally filtered by mastery status.
    Args:
        current_user: The username of the current user.
        mastered: Optional boolean to filter words by mastery status.

    Returns: A list of words for the current user, optionally filtered by mastery status.

    Raises:
        HTTPException: If the user does not exist.
    """
    existing_user = await get_user_by_username(current_user)

    if not existing_user:
        raise HTTPException(404, "User not exists")

    words = existing_user.get("words", []).copy()

    resultWords = []
    for word in words:
        if mastered is not None:
            if mastered and not word["mastered"] or not mastered and word["mastered"]:
                continue

        db_word = await get_word_id(word["word_id"])
        if not db_word:
            raise HTTPException(404, "Word not found.")

        resultWords.append(
            {
                "word_id": word["word_id"],
                "word": db_word.get("word"),
                "user_definition": word["user_definition"],
                "dictionary_meaning": db_word.get("meaning"),
                "mastered": word["mastered"],
            }
        )

    return {"words": resultWords}


@user_router.get("/word/{word_id}", status_code=200)
async def get_specific_word(word_id: str, current_user: str = Depends(decode_access_token)):
    """
    Retrieves the details of a specific word for the current user.
    Args:
        current_user: The username of the current user.
        word_id: The ID of the word to retrieve.

    Returns: The details of the specified word for the current user.

    Raises:
        HTTPException: If the user does not exist or if the word is not found for the user.
    """
    existing_user = await get_user_by_username(current_user)

    if not existing_user:
        raise HTTPException(404, "User not exists")

    words = existing_user.get("words", []).copy()
    word = next((word for word in words if word["word_id"] == word_id), None)

    if not word:
        raise HTTPException(404, "Word not found.")

    db_word = await get_word_id(word_id)
    if not db_word:
        raise HTTPException(404, "Word not found.")

    return {
        "word_id": word_id,
        "word": db_word.get("word"),
        "user_definition": word["user_definition"],
        "dictionary_meaning": db_word.get("meaning"),
        "mastered": word["mastered"],
    }


@user_router.put("/word/{word_id}", status_code=200)
async def update_specific_word(
    word_id: str,
    body: UserWordUpdate,
    current_user: str = Depends(decode_access_token),
):
    """
    Updates the details of a specific word for the current user.
    Args:
        current_user: The username of the current user.
        word_id: The ID of the word to update.
        body: The updated word information.

    Returns: A message indicating the success of the update.

    Raises:
        HTTPException: If the user does not exist, if the word is not found for the user, or if the request body is invalid.
    """
    if body.user_definition is None and body.mastered is None:
        raise HTTPException(400, "Invalid body.")

    existing_user = await get_user_by_username(current_user)

    if not existing_user:
        raise HTTPException(404, "User not exists")

    words = existing_user.get("words", [])

    target_word = next((w for w in words if w["word_id"] == word_id), None)

    if not target_word:
        raise HTTPException(404, "Word not found.")

    if body.mastered is not None:
        target_word["mastered"] = body.mastered

    if body.user_definition is not None:
        target_word["user_definition"] = body.user_definition

    updated_words = [target_word if w["word_id"] == word_id else w for w in words]

    await update_user(current_user, {"words": updated_words})

    return {"message": "Word updated successfully."}


@user_router.delete("/word/{word_id}", status_code=200)
async def delete_specific_word(word_id: str, current_user: str = Depends(decode_access_token)):
    """
    Deletes a specific word from the current user's list.
    Args:
        current_user: The username of the current user.
        word_id: The ID of the word to delete.

    Returns:
        A message indicating the success of the deletion.

    Raises:
        HTTPException: If the user does not exist or if the word is not found for the user.
    """
    existing_user = await get_user_by_username(current_user)

    if not existing_user:
        raise HTTPException(404, "User not exists")

    words = existing_user.get("words", []).copy()
    removed_words = [word for word in words if word["word_id"] != word_id]

    if len(words) == len(removed_words):
        raise HTTPException(404, "Word not found.")

    await update_user(current_user, {"words": removed_words})
    return {
        "message": f"Word removed successfully for user '{current_user}' successfully."
    }
