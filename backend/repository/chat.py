from sqlalchemy.orm import Session,selectinload
from sqlalchemy import select,func,exists,desc

from models import Chat,ChatMember,ChatType,User

class ChatRepository:

    """
    Cria um chat privado entre dois usuários.
    """
    def create_private_chat(
            self, 
            session: Session, 
            creator_id: int,
            other_user_id: int,
    ) -> Chat:
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

    """
    Cria um grupo com base numa lista de ids de usuários mais o criador
    """
    def create_group_chat(
            self,
            session: Session,
            creator_id: int,
            members_id: list[int],
            name: str,
            description: str,
    ) -> Chat:
        chat = Chat(
            name = name,
            description=description,
            type=ChatType.GROUP,
            created_by_id=creator_id
        )
        
        session.add(chat)
        #O flush envia o chat para o banco de dados, que gera um id para o chat
        session.flush()

        chat_members = [
            ChatMember(
                chat_id=chat.id,
                user_id=member_id,
                is_admin=False
            ) 
            for member_id in members_id
        ]

        chat_members.append(
            ChatMember(
                chat_id=chat.id,
                user_id=creator_id,
                is_admin=True
            )
        )

        session.add_all(chat_members)

        session.commit()
        
        return chat

    """
    Encontra um chat privado usando o id dos dois usuários.
    """
    def find_private_chat_between_users(
            self,
            session: Session,
            user_id_1: int,
            user_id_2: int
        ) -> Chat | None:
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

    """
    Verifica se o usuário faz parte de um chat.
    """
    def user_exists_in_chat(
            self,
            session: Session,
            user_id: int,
            chat_id: int
    ) -> bool:
        stmt = select(
            exists().where(
                ChatMember.chat_id == chat_id,
                ChatMember.user_id == user_id
            )
        )
        
        return session.scalar(stmt)

    """
    Pega todos os participantes de um chat
    """
    def get_users_in_chat(
            self,
            session: Session,
            chat_id: int
    ) -> list[User]:
        stmt = (select(User)
                .join(User.chats)
                .where(ChatMember.chat_id == chat_id)
            )

        return session.scalars(stmt).all()

    """
    Pega os chats de um usuário.
    """
    def get_user_chats(
            self,
            session: Session,
            user_id: int
    ) -> list[Chat] | None:
        stmt = (select(Chat)
                .join(Chat.members)
                .where(ChatMember.user_id == user_id)
                .options(
                    selectinload(Chat.members)
                    .selectinload(ChatMember.user)
                )
                .order_by(
                    desc(Chat.last_message_at),
                )
            )

        return session.scalars(stmt).all()