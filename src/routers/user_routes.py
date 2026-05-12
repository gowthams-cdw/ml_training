from fastapi import APIRouter, HTTPException

from models.user_models import UserAuth
from services.user_services import create_user, get_user_by_username
from utils.auth import (
    create_access_token,
    hash_password,
    verify_password,
)

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/create", status_code=201)
async def register_user(data: UserAuth):
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

    return {
        "success": True,
        "status_code": 201,
        "data": None,
        "message": "User created successfully."
    }


@user_router.post("/login")
async def login_user(data: UserAuth):
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

    return {
        "success": True,
        "status_code": 200,
        "data": create_access_token({"username": existing_user["username"]}),
        "message": "User logged in successfully."
    }
