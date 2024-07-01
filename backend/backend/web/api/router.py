from fastapi.routing import APIRouter

from backend.web.api import auth, docs, genres, models, monitoring, playlists, user

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(playlists.router, prefix="/playlists", tags=["playlists"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(genres.router, prefix="/genres", tags=["genres"])
