from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.db.base import Base


class Playlist(Base):
    __tablename__ = "playlist"
    spotify_id = Column(String(62), primary_key=True, index=True, nullable=False)
    id = Column(String(20), nullable=False, index=True)
    prompt = Column(String(200), nullable=False)
    model = Column(String(32), nullable=False)
    genres = Column(String(300), nullable=False)
    num_songs = Column(Integer(), nullable=False)
    popularity = Column(Integer(), nullable=False)
    owner_id = Column(
        String(62), ForeignKey("users.spotify_id"), nullable=False, index=True
    )
    owner = relationship("User", back_populates="playlists")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
