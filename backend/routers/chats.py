from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from security.dependencies import get_current_user
from schema import CreatePrivateChat, ChatListResponse,MessageListResponse,CreateGroupChat
from models import User
from services.chat import ChatService
from database.database import get_session

router = APIRouter(
    prefix="/api/chats",
    tags=["chats"]
)

chat_service = ChatService()

@router.post("/private",status_code=status.HTTP_201_CREATED)
async def create_private_chat(
    data: CreatePrivateChat,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return await chat_service.create_private_chat(
        session=session,
        other_user_id=data.user_id,
        current_user=current_user
    )

@router.post("/group",status_code=status.HTTP_201_CREATED)
async def create_group_chat(
    data: CreateGroupChat,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return chat_service.create_group_chat(
        session=session,
        data=data,
        current_user=current_user
    )

@router.get("/{chat_id}/messages",response_model=MessageListResponse)
async def get_message_history(
    chat_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return chat_service.get_message_history(
        session=session,
        chat_id=chat_id,
        current_user=current_user
    )

@router.get("/userchats",response_model=ChatListResponse)
async def get_user_chats(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return chat_service.get_user_chats(
        session=session,
        user=current_user
    )