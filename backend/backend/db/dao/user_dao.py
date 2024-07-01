from datetime import datetime
from typing import List, Optional

from fastapi import Depends
from loguru import logger
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.dependencies import get_db_session
from backend.db.models.user import User


class DatabaseError(Exception):
    """Exception raised for database-related errors."""


class UserDAO:
    """Class for accessing the user table table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create(
        self,
        id: str,
        spotify_id: str,
        spotify_token: str,
        spotify_refresh_token: str,
        spotify_token_created_at: datetime,
        email: str,
        username: str,
        register_date: datetime,
    ) -> Optional[User]:
        """
        Creates a user.

        :param user_id: ID of the user.
        :param spotify_id: Spotify ID of the user.
        :param spotify_token: Spotify token of the user.
        :param spotify_refresh_token: Spotify refresh token of the user.
        :param spotify_token_created_at: Timestamp when the Spotify token was created.
        :param email: Email of the user.
        :param username: Username of the user.
        :param register_date: Registration date of the user.
        :return: The created User object if successful, else None.
        """
        try:

            user = User(
                id=id,
                spotify_id=spotify_id,
                spotify_token=spotify_token,
                spotify_refresh_token=spotify_refresh_token,
                spotify_token_created_at=spotify_token_created_at,
                email=email,
                username=username,
                register_date=register_date,
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(
                user,
            )  # Refresh the instance to get the generated id
            logger.info(f"Added user: {user}")
            return user
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Database error while adding user: {e}")
            return None

    async def get_by_id(
        self,
        id: str,
    ) -> Optional[User]:
        """
        Get specific user ID

        :param id: id of user.
        :return: The user if found, else None.
        """
        query = select(User).where(User.id == id)
        try:
            result = await self.session.execute(query)
            user = result.scalars().first()
            if user:
                logger.info(f"Fetched user with id {id}: {user}")
            else:
                logger.info(f"No user found with id {id}")
            return user
        except Exception as e:
            logger.error(f"Error fetching user by id {id}: {e}")
            raise DatabaseError(f"Error fetching user by id {id}") from e

    async def get_by_spotify_id(
        self,
        spotify_id: str,
    ) -> Optional[User]:
        """
        Get specific user by Spotify ID.

        :param spotify_id: spotify_id of user.
        :return: The user if found, else None.
        """
        query = select(User).where(User.spotify_id == spotify_id)
        try:
            result = await self.session.execute(query)
            user = result.scalars().first()
            if user:
                logger.info(f"Fetched user with spotify_id {spotify_id}: {user}")
            else:
                logger.info(f"No user found with spotify_id {spotify_id}")
            return user
        except Exception as e:
            logger.error(f"Error fetching user by spotify_id {spotify_id}: {e}")
            raise DatabaseError(
                f"Error fetching user by spotify_id {spotify_id}",
            ) from e

    async def get_all_users(self, limit: int, offset: int) -> List[User]:
        """
        Get all users with limit/offset pagination.

        :param limit: limit of users.
        :param offset: offset of users.
        :return: stream of users.
        """
        raw_users = await self.session.execute(
            select(User).limit(limit).offset(offset),
        )

        return list(raw_users.scalars().fetchall())

    async def update_spotify_tokens(
        self,
        spotify_id: str,
        spotify_token: str,
        spotify_refresh_token: str,
        spotify_token_created_at: datetime,
    ) -> Optional[User]:
        """
        Update spotify_token, spotify_refresh_token, and spotify_token_created_at for a specific user.

        :param id: ID of the user.
        :param spotify_token: New Spotify token.
        :param spotify_refresh_token: New Spotify refresh token.
        :param spotify_token_created_at: New timestamp for token creation.
        :return: Updated user if successful.
        """
        try:
            # Create an update query
            stmt = (
                update(User)
                .where(User.spotify_id == spotify_id)
                .values(
                    spotify_token=spotify_token,
                    spotify_refresh_token=spotify_refresh_token,
                    spotify_token_created_at=spotify_token_created_at,
                )
                .execution_options(synchronize_session="fetch")
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            if result.rowcount == 0:
                logger.info(f"No user found with spotify_id {spotify_id}")
                raise Exception(f"No user found with spotify_id {spotify_id}")

            updated_user = await self.session.get(User, spotify_id)
            logger.info(f"User with spotify_id {spotify_id} has been updated")

            if not updated_user:
                logger.info(
                    f"User with spotify_id {spotify_id} could not be fetched after update"
                )
                raise Exception(
                    f"User with spotify_id {spotify_id} could not be fetched after update"
                )

            logger.info(f"Updated tokens for user spotify_id {spotify_id}")
            return updated_user

        except SQLAlchemyError as e:
            logger.error(f"Error updating tokens for user spotify_id {spotify_id}: {e}")
            raise DatabaseError(
                f"Error updating tokens for user spotify_id {spotify_id}"
            ) from e

    async def delete(
        self,
        spotify_id: str,
    ) -> bool:
        """
        Deletes specific User by spotify_id.

        :param spotify_id: spotify_id of the User.
        :return: True if deleted, else returns false.
        """
        query = select(User).where(User.spotify_id == spotify_id)
        try:
            result = await self.session.execute(query)
            user = result.scalars().first()
            if user:
                await self.session.delete(user)
                await self.session.commit()
                logger.info(f"Deleted user with spotify_id {spotify_id}")
                return True
            else:
                logger.info(f"No user found with spotify_id {spotify_id}")
                return False
        except SQLAlchemyError as e:
            logger.error(f"Error deleting user with spotify_id {spotify_id}: {e}")
            raise DatabaseError(
                f"Error deleting user with spotify_id {spotify_id}"
            ) from e
