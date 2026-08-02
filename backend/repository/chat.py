from sqlalchemy.orm import Session
from sqlalchemy import select,func,exists

from models import Chat,ChatMember,ChatType

class ChatRepository:
    def create_private_chat(
            self, 
            session: Session, 
            creator_id: int,
            other_user_id: int,
    ):
        chat = Chat(
            type=ChatType.PRIVATE,
            created_by_id=creator_id
        )

        session.add(chat)
        #O flush envia o chat para o banco de dados, que gera um id para o chat
        session.flush()

        session.add_all([
            ChatMember(
                chat_id=chat.id,
                user_id=creator_id,
                is_admin=False
            ),
            ChatMember(
                chat_id=chat.id,
                user_id=other_user_id,
                is_admin=False
            ),
        ])

        session.commit()
        
        return chat

    def find_private_chat_between_users(
            self,
            session: Session,
            user_id_1: int,
            user_id_2: int
        ):
        stmt = (select(Chat)
                .join(Chat.members)
                .where(
                    Chat.type == ChatType.PRIVATE,
                    ChatMember.user_id.in_([user_id_1,user_id_2])
                )
                .group_by(Chat.id)
                .having(func.count(ChatMember.user_id) == 2)
        )
        return session.scalar(stmt)

    def user_exists_in_chat(
            self,
            session: Session,
            user_id: int,
            chat_id: int
    ):
        stmt = select(
            exists().where(
                ChatMember.chat_id == chat_id,
                ChatMember.user_id == user_id
            )
        )
        
        return session.scalar(stmt)