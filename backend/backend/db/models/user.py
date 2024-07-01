from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.db.base import Base


class User(Base):
    __tablename__ = "users"
    spotify_id = Column(String(62), primary_key=True, index=True, nullable=False)
    id = Column(String(20), nullable=False, index=True)
    spotify_token = Column(String, nullable=False)
    spotify_refresh_token = Column(String, nullable=False)
    spotify_token_created_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
    )
    email = Column(String(100), nullable=True)
    username = Column(String(200), nullable=True)
    register_date = Column(DateTime(timezone=True), default=func.now())
    playlists = relationship(
        "Playlist",
        cascade="all,delete-orphan",
        back_populates="owner",
        uselist=True,
    )
