import os
from typing import Any, Dict, List

import spotipy
from fastapi_sso import SpotifySSO
from loguru import logger
from spotipy.oauth2 import SpotifyOAuth


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class SpotifyManager:
    """
    SpotifyManager is a singleton class that manages the Spotify API connection.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope: str,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
        )

    async def refresh_access_token(self, refresh_token: str):
        try:
            token_info = self.sp_oauth.refresh_access_token(refresh_token)
            return {
                "new_access_token": token_info["access_token"],
                "new_refresh_token": token_info["refresh_token"],
            }
        except Exception as e:
            logger.error(f"Error refreshing access token: {e}")
            raise

    def get_most_listened_tracks(
        self,
        access_token: str,
        limit: int = 20,
        time_range: str = "medium_term",
    ) -> List[Dict[str, Any]]:
        try:
            sp = spotipy.Spotify(auth=access_token)
            results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
            return results["items"]
        except Exception as e:
            logger.error(f"Error fetching most listened tracks: {e}")
            raise

    def get_most_listened_artists(
        self,
        access_token: str,
        limit: int = 20,
        time_range: str = "medium_term",
    ) -> List[Dict[str, Any]]:
        try:
            sp = spotipy.Spotify(auth=access_token)
            results = sp.current_user_top_artists(limit=limit, time_range=time_range)
            return results["items"]
        except Exception as e:
            logger.error(f"Error fetching most listened artists: {e}")
            raise


client_id = os.getenv("BACKEND_SPOTIFY_CLIENT_ID")
client_secret = os.getenv("BACKEND_SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("BACKEND_REDIRECT_URI")
scope = os.getenv("BACKEND_SCOPE")

spotify_manager = SpotifyManager(client_id, client_secret, redirect_uri, scope)

spotify_sso = SpotifySSO(
    client_id,
    client_secret,
    redirect_uri,
    allow_insecure_http=True,
    scope=scope,
)
