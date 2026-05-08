from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from config.env import get_env

BCRYPT_HASH = get_env("BCRYPT_HASH")
JWT_HASH = get_env("JWT_HASH")
EXPIRTY_MINUTES = get_env("EXPIRTY_MINUTES") or 60

if not JWT_HASH or not BCRYPT_HASH:
    raise ValueError("Secret Hashes not setted up.")

bearer_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Args:
        password: The plain text password to be hashed.

    Returns: The hashed password as a string.
    """
    return bcrypt.hashpw(password.encode("utf-8"), BCRYPT_HASH.encode("utf-8")).decode(
        "utf-8"
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a hashed password.
    Args:
        plain_password: The plain text password to verify.
        hashed_password: The hashed password to compare against.

    Returns: True if the password is correct, False otherwise.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(data: dict) -> str:
    """
    Creates an access token with the given data.
    Args:
        data: The data to include in the token.

    Returns: The encoded JWT token as a string.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=float(EXPIRTY_MINUTES))

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, JWT_HASH)


def decode_access_token(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    """
    Decodes an access token and returns the user ID.
    Args:
        token: The HTTP authorization credentials containing the token.

    Returns: The user ID extracted from the token.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        decoded = jwt.decode(token.credentials, JWT_HASH)

        user_id: str | None = decoded.get("username")

        if not user_id:
            raise HTTPException(401, "Invalid Token.")

        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
