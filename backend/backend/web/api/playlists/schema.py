from datetime import datetime
from typing import Optional, Sequence

from pydantic import BaseModel


class Config(BaseModel):
    """Model for configuration attached to playlist request and consequently its response."""

    model: str
    num_songs: Optional[int] = 10
    genres: Optional[Sequence[str]] = None
    popularity: Optional[int] = 50
    generate_genres: Optional[str] = None


class Context(BaseModel):
    """Model for context attached to playlist request and consequently its response."""

    spotify_id: Optional[str] = None
    created_at: Optional[datetime] = None


class PlaylistBase(BaseModel):
    prompt: str


class PlaylistGenerationRequest(PlaylistBase):
    """Model for requesting a generated playlist to the server."""

    config: Config
    context: Optional[Context] = None


class PlaylistGenerationResponse(PlaylistBase):
    """Model for returning a generated playlist to the client."""

    config: Config
    context: Optional[Context] = None


class ListPlaylistResponse(BaseModel):
    """Model for returning a list of PlaylistsResponse to the client."""

    playlists: Sequence[PlaylistGenerationResponse]


class Playlist(PlaylistBase):
    """Model for accesing and using Playlist objects from the DB."""

    id: str
    spotify_id: str
    model: str
    genres: Sequence[str]
    num_songs: int
    popularity: int
    owner_id: str
    created_at: datetime

    class Config:
        orm_mode = True
