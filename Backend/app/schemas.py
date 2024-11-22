from datetime import datetime
from pydantic import UUID4, BaseModel


class RoomCreate(BaseModel):
    name: str


class RoomResponse(BaseModel):
    room_id: UUID4
    name: str
    created_at: datetime


class UserCreate(BaseModel):
    username: str
    password: str


class MessageResponse(BaseModel):
    username: str
    content: str
    timestamp: datetime
