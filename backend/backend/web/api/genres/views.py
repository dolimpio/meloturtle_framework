from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from backend.db.models.user import User
from backend.services.recommendations_manager.recommendation_models.moodika.model_a.config import (
    genres,
)
from backend.web.api.auth.auth_utils import get_current_user

router = APIRouter()


@router.get("/")
async def get_genres(user: User = Depends(get_current_user)):
    """
    Endpoint to get all genres used for recommendations.
    """
    try:
        # Ensure user is authenticated
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized request")

        return genres
    except Exception as e:
        logger.error(f"Failed to fetch gneres: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch genres")
