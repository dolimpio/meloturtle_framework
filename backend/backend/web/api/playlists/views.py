import ast
import time
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from loguru import logger

from backend.db.dao.playlist_dao import PlaylistDAO
from backend.db.models.user import User
from backend.services.recommendations_manager.recommender_manager import (
    RecommenderManager,
)
from backend.web.api.auth.auth_utils import generate_short_uuid, get_current_user_sp
from backend.web.api.playlists.schema import (
    Config,
    Context,
    ListPlaylistResponse,
    Playlist,
    PlaylistGenerationRequest,
    PlaylistGenerationResponse,
)

router = APIRouter()
recommender_manager = RecommenderManager()


@router.get("/", response_model=Optional[ListPlaylistResponse])
async def get_playlists(
    max_results: Optional[int] = 10,
    page: Optional[int] = 1,
    user: User = Depends(get_current_user_sp),
    playlist_dao: PlaylistDAO = Depends(),
):
    """
    Retrieve a number of playlists from user.
    """
    try:
        # Ensure user is authenticated
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized request")

        playlists = await playlist_dao.get_page(
            owner_id=user.spotify_id,
            max_results=max_results,
            page=page,
        )

        logger.info("this is what is inside of the plyalists results" + str(playlists))
        playlist_responses = [
            PlaylistGenerationResponse(
                prompt=playlist.prompt,
                config=Config(
                    model=playlist.model,
                    num_songs=playlist.num_songs,
                    genres=ast.literal_eval(playlist.genres),
                    popularity=playlist.popularity,
                ),  # Populate with actual config data if available
                context=Context(
                    spotify_id=playlist.spotify_id,
                    created_at=playlist.created_at,
                ),  # Populate with actual context data if available
            )
            for playlist in playlists
        ]

        return ListPlaylistResponse(playlists=playlist_responses)
    except Exception as e:
        logger.error(f"Error retrieving playlists for user {user.spotify_id}: {e}")
        logger.info("exception cause" + str(e))
        logger.info("exception context" + str(e.__context__))
        logger.info("exception dict" + str(e.__dict__))
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.delete("/{spotify_id}")
async def delete_playlist(
    spotify_id: str,
    user: User = Depends(get_current_user_sp),
    playlist_dao: PlaylistDAO = Depends(),
):
    """
    Delete a playlist given its spotify_id.

    :param spotify_id: spotify_id of the playlist.
    :param playlist_dao: DAO for playlists.
    """

    # Validate the user
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized request")

    if not await playlist_dao.delete_by_spotify_id(spotify_id=spotify_id):
        raise HTTPException(status_code=500, detail="Failed to delete playlist")

    return "Playlist removed"


@router.get("/search", response_model=Optional[ListPlaylistResponse])
async def get_playlists(
    searchTerm: Optional[str] = "",
    user: User = Depends(get_current_user_sp),
    playlist_dao: PlaylistDAO = Depends(),
):
    """
    Retrieve a search of playlists from user.
    """
    try:
        # Ensure user is authenticated
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized request")

        playlists = await playlist_dao.search(
            owner_id=user.spotify_id,
            prompt=searchTerm,
        )

        logger.info("this is what is inside of the plyalists results" + str(playlists))
        playlist_responses = [
            PlaylistGenerationResponse(
                prompt=playlist.prompt,
                config=Config(
                    model=playlist.model,
                    num_songs=playlist.num_songs,
                    genres=ast.literal_eval(playlist.genres),
                    popularity=playlist.popularity,
                ),  # Populate with actual config data if available
                context=Context(
                    spotify_id=playlist.spotify_id,
                    created_at=playlist.created_at,
                ),  # Populate with actual context data if available
            )
            for playlist in playlists
        ]

        return ListPlaylistResponse(playlists=playlist_responses)
    except Exception as e:
        logger.error(f"Error retrieving playlists for user {user.spotify_id}: {e}")
        logger.info("exception cause" + str(e))
        logger.info("exception context" + str(e.__context__))
        logger.info("exception dict" + str(e.__dict__))
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.post("/generate", response_model=PlaylistGenerationResponse)
async def generate_playlist(
    new_playlist: PlaylistGenerationRequest,
    user: User = Depends(get_current_user_sp),
):
    """
    Creates a new playlist with the given prompt, config, and context.

    :param new_playlist: new playlist details.
    """

    try:
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized request")

        # Generate playlist using the recommender manager
        generated_playlist = recommender_manager.generate_playlist(
            prompt=new_playlist.prompt,
            config=new_playlist.config.dict(),
            context=new_playlist.context.dict(),
            access_token=user.spotify_token,
        )

        if not generated_playlist:
            logger.error("The playlist was not generated.")
            raise HTTPException(status_code=500, detail="Playlist generation failed")
        logger.info("Generated_playlist." + str(generated_playlist))

        # Simulate a delay to ensure Spotify processes the playlist
        time.sleep(2)

        config = Config(
            model=generated_playlist["config"].get("model"),
            num_songs=generated_playlist["config"].get("num_songs"),
            genres=generated_playlist["config"].get("genres"),
            popularity=generated_playlist["config"].get("popularity"),
            generate_genres=generated_playlist["config"].get("generate_genres"),
        )

        context = Context(
            spotify_id=generated_playlist["context"].get("spotify_id"),
            created_at=datetime.now(timezone.utc),
        )
        response = PlaylistGenerationResponse(
            prompt=generated_playlist.get("prompt"),
            config=config,
            context=context,
        )

        logger.debug(f"Response to be returned: {response}")

        return response

    except ValueError as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        logger.info("exception cause" + str(e.__cause__))
        logger.info("exception context" + str(e.__context__))
        logger.info("exception dict" + str(e.__dict__))
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )


@router.post("/save")
async def save_playlist(
    playlist_request: PlaylistGenerationRequest,
    user: User = Depends(get_current_user_sp),
    playlist_dao: PlaylistDAO = Depends(),
):
    """
    Save a generated playlist to the database.

    :param playlist_request: Details of the generated playlist.
    :param user: User object from the authentication dependency.
    :param playlist_dao: DAO for playlists.
    """

    try:
        # Validate the user
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized request")

        playlist_id = generate_short_uuid()

        # Validation

        new_playlist = Playlist(
            id=playlist_id,
            spotify_id=playlist_request.context.spotify_id,
            prompt=playlist_request.prompt,
            model=playlist_request.config.model,
            genres=playlist_request.config.genres,
            num_songs=playlist_request.config.num_songs,
            popularity=playlist_request.config.popularity,
            owner_id=user.spotify_id,
            created_at=playlist_request.context.created_at,
        )

        # Save the new playlist to the database
        created_playlist = await playlist_dao.create(
            id=new_playlist.id,
            spotify_id=new_playlist.spotify_id,
            prompt=new_playlist.prompt,
            model=new_playlist.model,
            genres=str(new_playlist.genres),
            num_songs=new_playlist.num_songs,
            popularity=new_playlist.popularity,
            owner_id=new_playlist.owner_id,
            created_at=new_playlist.created_at,
        )

        # Verify that the playlist was successfully created
        if not created_playlist:
            raise HTTPException(status_code=500, detail="Failed to save the playlist")

        config = Config(
            model=created_playlist.model,
            num_songs=created_playlist.num_songs,
            genres=ast.literal_eval(created_playlist.genres),
            popularity=created_playlist.popularity,
            generate_genres=playlist_request.config.generate_genres,
        )
        context = Context(
            spotify_id=created_playlist.spotify_id,
            created_at=created_playlist.created_at,
        )
        saved_playlist = PlaylistGenerationResponse(
            prompt=created_playlist.prompt,
            config=config,
            context=context,
        )

        logger.debug(f"Saved Playlist: {saved_playlist}")

        return "Playlist saved"

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        logger.exception("An unexpected error occurred")
        logger.info("exception cause" + e.__cause__)
        logger.info("exception context" + e.__context__)
        logger.info("exception dict" + e.__dict__)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )
