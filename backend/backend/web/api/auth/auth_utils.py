import base64
import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt
from jose.constants import ALGORITHMS
from jwt import InvalidTokenError
from loguru import logger

from backend.db.dao.user_dao import UserDAO
from backend.db.models.user import User
from backend.services.spotify_manager.spotify_manager import spotify_manager

SECRET_KEY = os.getenv(
    "BACKEND_SECRET_KEY",
    "51b5322b5a0df25f19fc7550747a686b2268df325516698d91f6f11c05296836",
)
SESSION_COOKIE_NAME = os.getenv("BACKEND_SESSION_COOKIE_NAME", "ml-auth-jwt")

COOKIE = APIKeyHeader(name="authorization")


class BearAuthException(Exception):
    pass


def generate_short_uuid(length=8):
    # Generate a UUID
    full_uuid = uuid.uuid4()
    # Encode the UUID using base64 to make it shorter
    short_uuid = base64.urlsafe_b64encode(full_uuid.bytes).rstrip(b"=").decode("ascii")
    # Return the first `length` characters
    return short_uuid[:length]


def create_access_token(user_id: str, spotify_id: str):
    to_encode = {
        "user_id": user_id,
        "spotify_id": spotify_id,
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHMS.HS256)
    return encoded_jwt


async def get_token_payload(session_token: str = Depends(COOKIE)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(session_token, SECRET_KEY, algorithms=[ALGORITHMS.HS256])
        user_id: str = payload.get("user_id")
        spotify_id: str = payload.get("spotify_id")
        if user_id is None or spotify_id is None:
            raise credentials_exception
        return {
            "user_id": user_id,
            "spotify_id": spotify_id,
        }
    except JWTError:
        raise BearAuthException("Token could not be validated")
    except InvalidTokenError:
        raise credentials_exception


async def get_current_user(
    user_dao: UserDAO = Depends(),
    session_token: str = Depends(COOKIE),
) -> Optional[User]:
    """
    Get specific user with session_token

    :param user_dao: Instance of UserDAO to access the database.
    :param session_token: Session token used for authentication.
    :return: The user if found, else None.
    """
    if not session_token:
        logger.warning("Session token is missing")
        return None

    try:
        userdata = await get_token_payload(session_token)
        user_id = userdata.get("user_id")
        if not user_id:
            logger.error("User ID not found in token payload")
            return None

        user = await user_dao.get_by_id(user_id)
        if not user:
            logger.warning(f"No user found with ID {user_id}")
            return None

        return user

    except BearAuthException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_sp(
    user_dao: UserDAO = Depends(),
    session_token: str = Depends(COOKIE),
) -> Optional[User]:
    """
    Get specific user with session_token that also needs spotify permissions

    :param user_dao: Instance of UserDAO to access the database.
    :param session_token: Session token used for authentication.
    :return: The user if found, else None.
    """
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session token is missing",
        )

    try:
        userdata = await get_token_payload(session_token)
    except BearAuthException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = userdata.get("user_id")
    spotify_id = userdata.get("spotify_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID not found in token payload",
        )

    user = await user_dao.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not spotify_access_token_valid(user.spotify_token_created_at):

        try:
            new_spotify_token_created_at = datetime.now(timezone.utc)
            new_info = await refresh_spotify_token(
                old_refresh_token=user.spotify_refresh_token,
            )
            user = await user_dao.update_spotify_tokens(
                spotify_id=spotify_id,
                spotify_token=new_info.get("new_access_token"),
                spotify_refresh_token=new_info.get("new_refresh_token"),
                spotify_token_created_at=new_spotify_token_created_at,
            )
            logger.info(f"User with id {user_id} has a new Spotify access token")

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error refreshing Spotify token: {str(e)}",
            )

    return user


def spotify_access_token_valid(since_time: datetime) -> bool:
    """
    Check if an hour has passed since the given time.

    :param since_time: A datetime object representing the starting time.
    :return: True if less an hour has passed, False otherwise.
    """
    current_time = datetime.now(timezone.utc)
    time_difference = current_time - since_time
    return time_difference < timedelta(hours=1)


async def refresh_spotify_token(old_refresh_token: str):
    new_info = await spotify_manager.refresh_access_token(old_refresh_token)
    new_access_token = new_info.get("new_access_token")
    new_refresh_token = new_info.get("new_refresh_token")
    if new_access_token and new_refresh_token:
        return new_info
    return None
