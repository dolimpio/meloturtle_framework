from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from backend.db.models.user import User
from backend.services.recommendations_manager.recommender_manager import (
    RecommenderManager,
)
from backend.web.api.auth.auth_utils import get_current_user
from backend.web.api.models.schema import RecommendationModel

router = APIRouter()

recommender_manager = RecommenderManager()


@router.get("/")
async def get_models(user: User = Depends(get_current_user)):
    """
    Endpoint to get all recommendation models.
    """
    try:
        # Ensure user is authenticated
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized request")

        models = recommender_manager.get_all_models()
        models_list = [
            {
                "name": model.name,
                "description": model.description,
                "version": model.version,
            }
            for model in models
        ]
        logger.info("Models fetched successfully" + str(models_list))
        return models_list
    except Exception as e:
        logger.error(f"Failed to fetch models: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch models")


@router.get("/names")
async def get_model_names(user: User = Depends(get_current_user)):
    """
    Endpoint to get all recommendation model names.
    """
    try:
        # Ensure user is authenticated
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized request")

        models = recommender_manager.get_all_models()

        model_names = [{"name": model.get_model_info()["name"]} for model in models]
        logger.info("Model names fetched successfully")
        return model_names
    except Exception as e:
        logger.error(f"Failed to fetch model names: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch model names")


@router.get("/{model_name}", response_model=RecommendationModel)
async def get_model_info(model_name: str, user: User = Depends(get_current_user)):
    """
    Endpoint to get information about a specific recommendation model.
    """
    try:
        # Ensure user is authenticated
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized request")

        model = recommender_manager.get_model_by_name(model_name)
        if model:
            logger.info(f"Model {model_name} fetched successfully")
            return model.get_model_info()
        else:
            raise HTTPException(status_code=404, detail="Model not found")
    except Exception as e:
        logger.error(f"Failed to fetch model {model_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch model")
