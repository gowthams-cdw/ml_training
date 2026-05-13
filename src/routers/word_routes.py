import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import StreamingResponse

from models.api_response import ApiResponse
from models.user_models import Vocabulary, VocabularyUpdate
from models.word_models import WordCreate
from services.user_services import get_user_by_username, update_user
from services.word_services import create_word, get_word, get_word_id
from utils.auth import decode_access_token

word_router = APIRouter(prefix="/words", tags=["words"])


@word_router.post("/", status_code=201, response_model=ApiResponse)
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

    new_word = Vocabulary(
        word_id=str(existing_word.get("id")),
        user_definition=body.word_meaning,
        mastered=False,
    )
    words = existing_user.get("words", []).copy()
    words.append(new_word.model_dump())

    await update_user(current_user, {"words": words})

    return {
        "success": True,
        "status_code": 201,
        "data": None,
        "message": f"Word '{body.word}' with {existing_word.get('id')} as id is added to user '{current_user}' successfully.",
    }


@word_router.get("/", status_code=200, response_model=ApiResponse)
async def get_all_words(
    mastered: bool | None = None, current_user: str = Depends(decode_access_token)
):
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

    async def event_stream():
        static_words = [
            {
                "word_id": word["word_id"],
                "word": word["word"],
                "user_definition": word["user_definition"],
                "mastered": word["mastered"],
            }
            for word in resultWords
        ]
        yield f"event: meta\ndata: {json.dumps({'success': True, 'status_code': 200, 'message': 'Words fetched successfully.', 'words': static_words})}\n\n"

        for w in resultWords:
            yield f"event: definition_start\ndata: {json.dumps({'word_id': w['word_id']})}\n\n"

            for chunk in w["dictionary_meaning"].split():
                yield f"event: chunk\ndata: {json.dumps({'word_id': w['word_id'], 'token': chunk + ' '})}\n\n"

            yield f"event: definition_end\ndata: {json.dumps({'word_id': w['word_id']})}\n\n"

        yield "event: done\ndata: {}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@word_router.get("/{word_id}", status_code=200, response_model=ApiResponse)
async def get_specific_word(
    word_id: str, current_user: str = Depends(decode_access_token)
):
    existing_user = await get_user_by_username(current_user)
    if not existing_user:
        raise HTTPException(404, "User not exists")

    words = existing_user.get("words", []).copy()
    word = next((w for w in words if w["word_id"] == word_id), None)
    if not word:
        raise HTTPException(404, "Word not found.")

    db_word = await get_word_id(word_id)
    if not db_word:
        raise HTTPException(404, "Word not found.")

    async def event_stream():
        yield f"event: meta\ndata: {json.dumps({'success': True, 'status_code': 200, 'message': 'Word fetched successfully.', 'word_id': word_id, 'word': db_word.get('word'), 'user_definition': word['user_definition'], 'mastered': word['mastered']})}\n\n"

        for chunk in db_word.get("meaning", "").split():
            yield f"event: chunk\ndata: {json.dumps({'token': chunk + ' '})}\n\n"

        yield "event: done\ndata: {}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@word_router.put("/{word_id}", status_code=200, response_model=ApiResponse)
async def update_specific_word(
    word_id: str,
    body: VocabularyUpdate,
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

    return {
        "success": True,
        "status_code": 200,
        "data": None,
        "message": "Word updated successfully.",
    }


@word_router.delete("/{word_id}", status_code=200, response_model=ApiResponse)
async def delete_specific_word(
    word_id: str, current_user: str = Depends(decode_access_token)
):
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
        "success": True,
        "status_code": 200,
        "data": None,
        "message": f"Word removed successfully for user '{current_user}' successfully.",
    }
