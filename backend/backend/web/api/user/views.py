from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from loguru import logger

from backend.db.dao.user_dao import UserDAO
from backend.db.models.user import User
from backend.web.api.auth.auth_utils import get_current_user
from backend.web.api.user.schema import UserResponse

router = APIRouter()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_dao: UserDAO = Depends(),
    *,
    user_id: str,
    user: User = Depends(get_current_user),
) -> dict:
    """
    Retrieve a single user by its ID.
    """
    try:
        # Ensure user is authenticated
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized request")

        user = await user_dao.get_by_id(user_id)
        logger.info(f"User with id {user_id} has been recovered")

        if not user:
            raise HTTPException(status_code=404, detail=f"User not found")
        else:
            return_user = UserResponse(
                id=user.id,
                spotify_id=user.spotify_id,
                email=user.email,
                username=user.username,
                register_date=user.register_date,
            )
            return return_user

    # except DatabaseError as e:
    #     raise HTTPException(status_code=500, detail=f"An unexpected error occurred. Report this message to support.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )
