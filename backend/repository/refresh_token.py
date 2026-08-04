from sqlalchemy import select
from sqlalchemy.orm import Session

from models import RefreshToken

class RefreshTokenRepository:
    def create(
            self,
            session: Session,
            token: RefreshToken,
        ):
        session.add(token)
        session.commit()

        return token

    def get_by_hash(            
            self,
            session: Session,
            token_hash: str
        ):
        stmt = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash
        )

        return session.scalar(stmt)

    def revoke(
            self,
            session: Session,
            token: RefreshToken,
    ):
        token.revoked = True
        session.commit()
