from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from repository import ChatRepository,UserRepository,MessageRepository 
from models import User,ChatType
from schema import ChatListResponse, ChatListItem,MessageListItem, MessageListResponse,CreateGroupChat

class ChatService:
    def __init__(self):
        self.chat_repository = ChatRepository()
        self.user_repository = UserRepository()
        self.message_repository = MessageRepository()

    """
    Cria um chat privado entre o usuário atual
    e outro usuário com base no id do outro usuário
    """
    def create_private_chat(
            self, 
            session: Session, 
            current_user: User,
            other_user_id: int
        ):

        if other_user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CANNOT_CREATE_CHAT_ALONE"
            )

        if other_user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CANNOT_CHAT_WITH_YOURSELF"
            )
        
        if self.chat_repository.find_private_chat_between_users(
            session=session,
            user_id_1=current_user.id,
            user_id_2=other_user_id
        ) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CHAT_ALREADY_EXISTS"
            )
        
        if self.user_repository.get_by_id(session,other_user_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="USER_NOT_FOUND"
            )
            
        chat = self.chat_repository.create_private_chat(
            session=session,
            creator_id=current_user.id,
            other_user_id=other_user_id
        )
    
        return { #TODO
            "message":"Chat criado com sucesso",
            "chat_id":chat.id
        }

    def create_group_chat(
            self,
            session: Session,
            data: CreateGroupChat,
            current_user: User
    ):
        if data.user_ids is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CANNOT_CREATE_CHAT_ALONE"
            )

        if current_user.id in data.user_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CREATOR_ALREADY_IN_MEMBERS"
            )
        if len(data.user_ids) != len(set(data.user_ids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="REPEATED_ID"
            )

        for user_id in data.user_ids:
            if self.user_repository.get_by_id(session,user_id) is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="USER_NOT_FOUND"
                )
        
        chat = self.chat_repository.create_group_chat(
            session=session,
            creator_id=current_user.id,
            members_id=data.user_ids,
            name=data.name,
            description=data.description
        )

        return { #TODO
            "message":"Chat criado com sucesso",
            "chat_id":chat.id
        }
        

    """
    Pega as mensagens passadas de um chat em que
    o usuário atual esteja participando
    """
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
                status_code=status.HTTP_403_FORBIDDEN,
                detail="USER_NOT_IN_CHAT"
            )

        chat_history = self.message_repository.get_chat_history(
            session=session,
            chat_id=chat_id
        )
        chat_messages = []
        for message in chat_history:
            chat_messages.append(MessageListItem(
                id=message.id,
                message=message.message,
                chat_id=message.chat_id,
                sender_id=message.sender_id,
                created_at=message.created_at
            ))
        return MessageListResponse(
            messages=chat_messages
        )

    """
    Retorna os usuários em um chat
    """
    def get_users_in_chat(
            self,
            session: Session,
            chat_id: int
    ) -> list[User]:
        return self.chat_repository.get_users_in_chat(
            session=session,
            chat_id=chat_id
        )

    """
    Retorna os chats do usuário
    """
    def get_user_chats(
            self,
            session: Session,
            user: User
    ):
        chats = self.chat_repository.get_user_chats(
            session=session,
            user_id=user.id
        )

        chat_items = []

        for chat in chats:
            #Caso o chat seja privado o nome do chat será do outro usuário
            #Isso porque um chat privado não tem nome na database
            if chat.type == ChatType.PRIVATE:
                for member in chat.members:
                    if user.id != member.user_id:
                        display_name = member.user.username
                        break
            else:
                display_name = chat.name

            chat_items.append(
                ChatListItem(
                    id=chat.id,
                    description=chat.description,
                    type=chat.type,
                    display_name=display_name,
                    users_id=[member.user_id for member in chat.members]
                )
            )

        return ChatListResponse(chats=chat_items)