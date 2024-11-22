from uuid import uuid4
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import List

from pydantic import UUID4

from app.schemas import MessageResponse, RoomCreate, RoomResponse, UserCreate
from app.models import User, Room, Message
from app.utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
    verify_token,
    oauth2_scheme,
)


# Configuração
router = APIRouter()


# Rotas
@router.get("/users/me")
def get_me(current_username: str = Depends(get_current_user)):
    user = User.objects(username=current_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"username": user.username}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User.objects(username=form_data.username).first()
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users", response_model=dict)
def create_user(user: UserCreate):
    if User.objects(username=user.username).first():
        raise HTTPException(status_code=400, detail="Usuário já existe")
    User.create(username=user.username, password=user.password)
    return {"message": "Usuário criado com sucesso"}


@router.post("/rooms", response_model=RoomResponse)
def create_room(room: RoomCreate, token: str = Depends(oauth2_scheme)):
    verify_token(token)
    new_room = Room.create(name=room.name)
    return RoomResponse(
        room_id=new_room.room_id, name=new_room.name, created_at=new_room.created_at
    )


@router.get("/rooms", response_model=List[RoomResponse])
def list_rooms(token: str = Depends(oauth2_scheme)):
    verify_token(token)
    rooms = Room.objects.all()
    return [
        RoomResponse(room_id=room.room_id, name=room.name, created_at=room.created_at)
        for room in rooms
    ]


@router.get("/rooms/{room_id}", response_model=RoomResponse)
def get_room(room_id: str, token: str = Depends(oauth2_scheme)):
    verify_token(token)
    room = Room.objects(room_id=room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    return RoomResponse(
        room_id=room.room_id, name=room.name, created_at=room.created_at
    )


@router.get("/rooms/{room_id}/messages", response_model=List[MessageResponse])
def get_messages(room_id: str, token: str = Depends(oauth2_scheme)):
    verify_token(token)
    messages = Message.objects(room_id=room_id).all()
    return [
        MessageResponse(
            username=msg.username, content=msg.content, timestamp=msg.timestamp
        )
        for msg in messages
    ]


@router.post("/rooms/{room_id}/message/")
def send_message(
    room_id: UUID4,
    content: str,
    token: str = Depends(oauth2_scheme),
    current_username: str = Depends(get_current_user),
):
    user = User.objects(username=current_username).first()
    verify_token(token)
    try:
        Message.create(room_id=room_id, username=user.username, content=content)
        return {"room_id": room_id, "username": user.username, "content": content}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")


@router.put("/rooms/{room_id}", response_model=RoomResponse)
def update_room(room_id: UUID4, room: RoomCreate, token: str = Depends(oauth2_scheme)):
    verify_token(token)
    existing_room = Room.objects(id=room_id).first()
    if not existing_room:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    existing_room.update(name=room.name)
    return RoomResponse(
        room_id=existing_room.room_id,
        name=existing_room.name,
        created_at=existing_room.created_at,
    )


@router.delete("/rooms/{room_id}")
def delete_room(room_id: UUID4, token: str = Depends(oauth2_scheme)):
    verify_token(token)
    room = Room.objects(id=room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    room.delete()
    return {"message": "Sala excluída com sucesso"}
