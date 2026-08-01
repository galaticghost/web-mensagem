from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from security.dependencies import get_current_user
from schema.chat import CreatePrivateChat
from models import User
from repository.chat import ChatRepository
from database.database import get_session

router = APIRouter(
    prefix="/api/chats",
    tags=["chats"]
)
chat_repository = ChatRepository()

@router.post("/private",status_code=status.HTTP_201_CREATED)
async def create_private_chat(
    data: CreatePrivateChat,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if data.user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Não é possível criar um chat consigo mesmo."
    )

    #TODO Ver se não já existe chat
    #TODO Ver se o outro usuário existe(o current_user já sabe por conta da função)
    
    chat = chat_repository.create_private_chat(
        session=session,
        creator_id=current_user.id,
        other_user_id=data.user_id
    )

    return {
        "message":"Chat criado com sucesso",
        "chat_id":chat.id
    }