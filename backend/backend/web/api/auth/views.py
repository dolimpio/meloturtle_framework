import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from loguru import logger
from starlette.requests import Request

from backend.db.dao.user_dao import DatabaseError, UserDAO
from backend.services.spotify_manager.spotify_manager import spotify_sso
from backend.web.api.auth.auth_utils import (
    SESSION_COOKIE_NAME,
    create_access_token,
    generate_short_uuid,
    refresh_spotify_token,
    spotify_access_token_valid,
)
from backend.web.api.user.schema import UserCreate

directory_path = Path(__file__).parent
env_file_path = directory_path.parents[3] / ".env"

load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("BACKEND_SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("BACKEND_SPOTIFY_CLIENT_SECRET")
SCOPE = os.getenv("BACKEND_SCOPE")
REDIRECT_URI = os.getenv("BACKEND_REDIRECT_URI")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


router = APIRouter()


@router.get("/")
async def spotify_login():
    return await spotify_sso.get_login_redirect()


@router.get("/callback")
async def spotify_callback(request: Request, user_dao: UserDAO = Depends()):
    """Process login response from Spotify and return user info"""

    try:
        spotify_token_created_at = datetime.now(timezone.utc)
        user = await spotify_sso.verify_and_process(request)
        user_stored = await user_dao.get_by_spotify_id(user.id)
        logger.info(f"No user found with spotify_id{user_stored}")

        if not user_stored:
            logger.info("Non existent user will be created")

            user_id = generate_short_uuid()
            # Validates data with pydantic
            user_to_add = UserCreate(
                id=user_id,
                spotify_id=user.id,
                spotify_token=spotify_sso.access_token,
                spotify_refresh_token=spotify_sso.refresh_token,
                spotify_token_created_at=spotify_token_created_at,
                email=user.email,
                username=user.display_name,
                register_date=datetime.now(timezone.utc),
            )
            # We add the user to the database
            user_stored = await user_dao.create(
                id=user_to_add.id,
                spotify_id=user_to_add.spotify_id,
                spotify_token=user_to_add.spotify_token,
                spotify_refresh_token=user_to_add.spotify_refresh_token,
                spotify_token_created_at=user_to_add.spotify_token_created_at,
                email=user_to_add.email,
                username=user_to_add.username,
                register_date=user_to_add.register_date,
            )
            logger.info("Non existent user was created")

        elif not spotify_access_token_valid(user_stored.spotify_token_created_at):
            logger.info("token will be updated")

            new_spotify_token_created_at = datetime.now(timezone.utc)
            new_info = await refresh_spotify_token(
                old_refresh_token=user_stored.spotify_refresh_token,
            )
            user_stored = await user_dao.update_spotify_tokens(
                spotify_id=user_stored.spotify_id,
                spotify_token=new_info.get("new_access_token"),
                spotify_refresh_token=new_info.get("new_refresh_token"),
                spotify_token_created_at=new_spotify_token_created_at,
            )
            logger.info("token was updated")

        access_token = create_access_token(
            user_id=user_stored.id,
            spotify_id=user_stored.spotify_id,
        )
        response = RedirectResponse(
            url="http://localhost:3000/redirect",
            status_code=status.HTTP_302_FOUND,
        )
        response.set_cookie(SESSION_COOKIE_NAME, access_token)

        return response

    except DatabaseError as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support.",
        )
    except ValueError as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred cause: {e.__cause__}")
        logger.error(f"An unexpected error occurred context: {e.__context__}")

        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )
