from typing import Optional

from pydantic import BaseModel


class UserWord(BaseModel):
    """
    A model representing a user's word entry.
    Attributes:
        word_id: The unique identifier for the word.
        user_definition: The user's definition for the word.
        mastered: Whether the user has mastered the word.
    """

    word_id: str
    user_definition: str
    mastered: bool


class User(BaseModel):
    """
    A model representing a user.
    Attributes:
        username: The user's username.
        password: The user's password.
        words: A list of the user's word entries.
    """

    username: str
    password: str
    words: list[UserWord]


class UserAuth(BaseModel):
    """
    A model representing the data required to authenticate/create a user.
    Attributes:
        username: The user's username.
        password: The user's password.
    """

    username: str
    password: str


class UserWordUpdate(BaseModel):
    """
    A model representing the data required to update a user's word entry.
    Attributes:
        user_definition: The user's updated definition for the word.
        mastered: The user's updated mastery status for the word.
    """

    user_definition: Optional[str]
    mastered: Optional[bool]


class UserIdResponse(BaseModel):
    """
    A model representing the response data containing a user's unique identifier.
    Attributes:
        id: The user's unique identifier.
    """

    id: str


class LoginUserResponse(BaseModel):
    """
    A model representing the response data for a successful user login.
    Attributes:
        token: The authentication token.
    """

    token: str
