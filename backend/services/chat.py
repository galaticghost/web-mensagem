from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from repository import ChatRepository,UserRepository,MessageRepository 
from models import User,ChatType,Chat
from schema import ChatListResponse, ChatListItem,MessageListItem, MessageListResponse,CreateGroupChat
from ws.connection_manager import connection_manager

class ChatService:
    def __init__(self):
        self.chat_repository = ChatRepository()
        self.user_repository = UserRepository()
        self.message_repository = MessageRepository()

    """
    Cria um chat privado entre o usuário atual
    e outro usuário com base no id do outro usuário
    """
    async def create_private_chat(
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

        other_user = self.user_repository.get_by_id(
            session,
            other_user_id
        )
        
        if other_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="USER_NOT_FOUND"
            )
            
        chat = self.chat_repository.create_private_chat(
            session=session,
            creator_id=current_user.id,
            other_user_id=other_user_id
        )

        chat_item = self._build_chat_list_item(
            chat=chat,
            user=other_user
        )

        data = {
            "type": "new_chat",
            "content":  chat_item.model_dump(mode="json")
        }

        await connection_manager.send_to_users(
            users_id=[other_user_id],
            data=data
        )
    
        return { #TODO
            "message":"Chat criado com sucesso",
            "chat_id":chat.id
        }

    async def create_group_chat(
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

        return ChatListResponse(
            chats=[
                self._build_chat_list_item(chat, user)
                for chat in chats
            ]
        )

    def _build_chat_list_item(
            self,
            chat: Chat,
            user: User
        ) -> ChatListItem:

        #Caso o chat seja privado o nome do chat será do outro usuário
        #Isso porque um chat privado não tem nome na database
        if chat.type == ChatType.PRIVATE:
            for member in chat.members:
                if member.user_id != user.id:
                    display_name = member.user.username
                    break
        else:
            display_name = chat.name

        return ChatListItem(
            id=chat.id,
            description=chat.description,
            type=chat.type,
            display_name=display_name,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
            last_message_id=chat.last_message_id,
            last_message_at=chat.last_message_at,
            users_id=[member.user_id for member in chat.members]
        )