from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User

class UserRepository:
    """
    Pega o usuário com base no id
    """
    def get_by_id(self,session: Session, id: int) -> User | None:
        stmt = select(User).where(User.id == id)
        return session.scalar(stmt)

    """
    Pega o usuário com base no email
    """
    def get_by_email(self, session: Session, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return session.scalar(stmt)

    """
    Pega o usuário com base no nome de usuário
    """
    def get_by_username(self, session: Session, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return session.scalar(stmt)

    #TODO tirar o próprio usuário ou talvez não ou sim depende
    def search_by_username(self,session: Session, username: str) -> list[User] | None:
        stmt = (
            select(User)
            .where(User.username.ilike(f'{username}%'))
            .order_by(User.username)
        )
        return session.scalars(stmt).all()

    """
    Cria o usuário, comita a transação e atualiza o objeto usuário
    com base nas novas informações do banco e o retorna.
    """
    def create(self, session: Session, user: User) -> User:
        session.add(user)
        session.commit()
        session.refresh(user)

        return user