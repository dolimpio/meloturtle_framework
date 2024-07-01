from datetime import datetime
from typing import List, Optional

from fastapi import Depends
from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.dependencies import get_db_session
from backend.db.models.playlist import Playlist


class DatabaseError(Exception):
    """Exception raised for database-related errors."""


class PlaylistDAO:
    """Class for accessing the playlist table table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create(
        self,
        prompt: str,
        id: str,
        spotify_id: str,
        model: str,
        genres: str,
        num_songs: int,
        popularity: int,
        owner_id: str,
        created_at: datetime,
    ) -> Optional[Playlist]:
        """
        Creates a playlist.

        :param prompt: Description of the playlist.
        :param id: ID of the playlist.
        :param spotify_id: Spotify ID of the playlist.
        :param model: Model used for the playlist.
        :param genres: List of genres associated with the playlist.
        :param owner_id: ID of the owner of the playlist.
        :param created_at: Timestamp when the playlist was created.
        :return: The created Playlist object if successful, else None.
        """
        try:
            playlist = Playlist(
                prompt=prompt,
                id=id,
                spotify_id=spotify_id,
                model=model,
                genres=genres,
                num_songs=num_songs,
                popularity=popularity,
                owner_id=owner_id,
                created_at=created_at,
            )
            self.session.add(playlist)
            await self.session.commit()
            await self.session.refresh(
                playlist,
            )  # Refresh the instance to get the generated id
            logger.info(f"Added playlist: {playlist}")
            return playlist
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Database error while adding playlist: {e}")
            return None

    async def get_by_id(
        self,
        id: str,
    ) -> Optional[Playlist]:
        """
        Get specific Playlist by ID

        :param id: id of the Playlist.
        :return: The Playlist if found, else None.
        """
        query = select(Playlist).where(Playlist.id == id)
        try:
            result = await self.session.execute(query)
            playlist = result.scalars().first()
            if playlist:
                logger.info(f"Fetched Playlist with id {id}: {playlist}")
            else:
                logger.info(f"No Playlist found with id {id}")
            return playlist
        except Exception as e:
            logger.error(f"Error fetching playlist by id {id}: {e}")
            raise DatabaseError(f"Error fetching playlist by id {id}") from e

    async def get_by_spotify_id(
        self,
        spotify_id: str,
    ) -> Optional[Playlist]:
        """
        Get specific Playlist by Spotify ID.

        :param spotify_id: spotify_id of Playlist.
        :return: The Playlist if found, else None.
        """
        query = select(Playlist).where(Playlist.spotify_id == spotify_id)
        try:
            result = await self.session.execute(query)
            playlist = result.scalars().first()
            if playlist:
                logger.info(
                    f"Fetched Playlist with spotify_id {spotify_id}: {playlist}",
                )
            else:
                logger.info(f"No Playlist found with spotify_id {spotify_id}")
            return playlist
        except Exception as e:
            logger.error(f"Error fetching Playlist by spotify_id {spotify_id}: {e}")
            raise DatabaseError(
                f"Error fetching Playlist by spotify_id {spotify_id}",
            ) from e

    async def get_playlist_owned_by(
        self,
        owner_id: str,
        max_results: Optional[int] = 10,
    ) -> List[Playlist]:
        """
        Get playlists by owner ID.

        :param owner_id: ID of the owner.
        :param max_results: Maximum number of results to return.
        :return: List of Playlists.
        """
        query = select(Playlist).where(Playlist.owner_id == owner_id).limit(max_results)
        try:
            result = await self.session.execute(query)
            playlists = result.scalars().all()
            logger.info(f"Fetched {len(playlists)} playlists for owner_id {owner_id}")
            return playlists
        except SQLAlchemyError as e:
            logger.error(f"Error fetching Playlists for owner_id {owner_id}: {e}")
            raise DatabaseError(
                f"Error fetching Playlists for owner_id {owner_id}",
            ) from e

    async def get_page(
        self,
        owner_id: str,
        max_results: Optional[int] = 10,
        page: Optional[int] = 1,
    ) -> List[Playlist]:
        """
        Get specific playlists based on the prompt and owner ID.

        :param owner_id: ID of the owner.
        :param prompt: Part or whole prompt of the playlist.
        :param max_results: Maximum number of results to return.
        :param page: Page number for pagination.
        :return: List of playlists matching the prompt and owner ID.
        """
        offset = (page - 1) * max_results
        query = (
            select(Playlist)
            .where(
                Playlist.owner_id == owner_id,
            )
            .offset(offset)
            .limit(max_results)
        )

        try:
            rows = await self.session.execute(query)
            logger.info(f"Fetched playlists for owner_id {owner_id}")
            return list(rows.scalars().fetchall())
        except SQLAlchemyError as e:
            logger.error(f"Error fetching Playlists: {e}")
            raise DatabaseError(
                f"Error fetching Playlists",
            ) from e

    async def search(
        self,
        owner_id: str,
        prompt: str,
    ) -> List[Playlist]:
        """
        Get specific playlists based on the prompt and owner ID.

        :param owner_id: ID of the owner.
        :param prompt: Part or whole prompt of the playlist.
        :param max_results: Maximum number of results to return.
        :param page: Page number for pagination.
        :return: List of playlists matching the prompt and owner ID.
        """
        query = select(Playlist).where(
            Playlist.owner_id == owner_id,
            Playlist.prompt.ilike(f"%{prompt}%"),
        )

        try:
            rows = await self.session.execute(query)
            logger.info(
                f"Fetched playlists for owner_id {owner_id} with prompt '{prompt}'"
            )
            return list(rows.scalars().fetchall())
        except SQLAlchemyError as e:
            logger.error(f"Error fetching Playlists with prompt '{prompt}': {e}")
            raise DatabaseError(
                f"Error fetching Playlists with prompt '{prompt}'",
            ) from e

    async def delete_by_id(
        self,
        id: str,
    ) -> bool:
        """
        Deletes specific Playlist by ID.

        :param id: ID of Playlist.
        :return: True if deleted, else returns false.
        """
        query = select(Playlist).where(Playlist.id == id)
        try:
            result = await self.session.execute(query)
            playlist = result.scalars().first()
            if playlist:
                await self.session.delete(playlist)
                logger.info(f"Deleted Playlist with id {id}")
                return True
            else:
                logger.info(f"No Playlist found with id {id}")
                return False
        except SQLAlchemyError as e:
            logger.error(f"Error deleting Playlist with id {id}: {e}")
            raise DatabaseError(f"Error deleting Playlist with id {id}") from e

    async def delete_by_spotify_id(
        self,
        spotify_id: str,
    ) -> bool:
        """
        Deletes specific Playlist by spotify_id.

        :param spotify_id: spotify_id of Playlist.
        :return: True if deleted, else returns false.
        """
        query = select(Playlist).where(Playlist.spotify_id == spotify_id)

        try:
            result = await self.session.execute(query)
            playlist = result.scalars().first()
            logger.info(f"FOUND PLAYLIST {playlist}")

            if playlist:
                await self.session.delete(playlist)
                logger.info(f"Deleted Playlist with spotify_id {spotify_id}")
                return True
            else:
                logger.info(f"No Playlist found with spotify_id {spotify_id}")
                return False
        except SQLAlchemyError as e:
            logger.info("exception cause DAO" + str(e.__cause__))
            logger.info("exception context DAO" + str(e.__context__))
            logger.info("exception dict DAO" + str(e.__dict__))
            logger.error(f"Error deleting Playlist with spotify_id {spotify_id}: {e}")
            raise DatabaseError(
                f"Error deleting Playlist with spotify_id {spotify_id}"
            ) from e
