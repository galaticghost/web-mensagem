from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User

class UserRepository:
    def get_by_email(self, session: Session, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return session.scalar(stmt)

    def get_by_username(self, session: Session, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return session.scalar(stmt)
    #TODO tirar o próprio usuário
    def search_by_username(self,session: Session, username: str) -> list[User] | None:
        stmt = (
            select(User)
            .where(User.username.ilike(f'{username}%'))
            .order_by(User.username)
        )
        return session.scalars(stmt).all()

    def create(self, session: Session, user: User):
        session.add(user)
        session.commit()
        session.refresh(user)

        return user