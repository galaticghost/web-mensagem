from fastapi import HTTPException
from sqlalchemy.orm import Session

from repository import ChatRepository, UserRepository, MessageRepository 
from models import User
from schema.chat import CreatePrivateChat

class ChatService:
    def __init__(self):
        self.chat_repository = ChatRepository()
        self.user_repository = UserRepository()
        self.message_repository = MessageRepository()

    def create_private_chat(
            self, 
            session: Session, 
            current_user: User,
            data: CreatePrivateChat
        ):

        if data.user_id == current_user.id:
            raise HTTPException(
                status_code=400,
                detail="Não é possível criar um chat consigo mesmo."
            )
        
        if self.chat_repository.find_private_chat_between_users(
            session=session,
            user_id_1=current_user.id,
            user_id_2=data.user_id
        ) is not None:
            raise HTTPException(
                status_code=400,
                detail="O chat entre os dois já existe"
            )
        
        if self.user_repository.get_by_id(session,data.user_id) is None:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado"
            )
            
        chat = self.chat_repository.create_private_chat(
            session=session,
            creator_id=current_user.id,
            other_user_id=data.user_id
        )
    
        return {
            "message":"Chat criado com sucesso",
            "chat_id":chat.id
        }

    def get_message_history(
            self,
            session: Session,
            chat_id: int,
            current_user: User
    ):
        if not self.chat_repository.user_exists_in_chat(
            session=session,
            user_id=current_user.id,
            chat_id=chat_id
        ):
            raise HTTPException(
                status_code=403,
                detail="O usuário não pertence a esse chat"
            )

        chat_history = self.message_repository.get_chat_history(
            session=session,
            chat_id=chat_id
        )

        return {"messages": chat_history}

