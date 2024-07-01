from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    spotify_token: str
    spotify_refresh_token: str
    spotify_token_created_at: datetime


# Properties to receive via API on creation
class UserCreate(UserBase):
    id: str
    spotify_id: str
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    register_date: datetime


# Properties to return via API
class UserResponse(BaseModel):
    id: str
    spotify_id: str
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    register_date: datetime
