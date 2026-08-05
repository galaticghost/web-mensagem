from fastapi import HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

from repository import UserRepository,RefreshTokenRepository
from models import User, RefreshToken
from security.jwt import create_access_token, create_refresh_token, hash_token
from schema import UserCreate,UserLogin,RefreshRequest

password_hash = PasswordHash.recommended()

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.refresh_token_repository = RefreshTokenRepository()

    def register(self, session: Session, data: UserCreate):
        if self.user_repository.get_by_email(session,data.email) is not None:
                raise HTTPException(
                    status_code=409,
                    detail="EMAIL_ALREADY_EXISTS"
                )
        
        if self.user_repository.get_by_username(session,data.username) is not None:
            raise HTTPException(
                status_code=409,
                detail="USERNAME_ALREADY_EXISTS"
            )
    
        user = User(
            username=data.username,
            email=data.email,
            password_hash=password_hash.hash(data.password)
        )
    
        self.user_repository.create(session,user)
        return {"message": "Usuário criado com sucesso"}

    def login(self, session: Session, data:UserLogin):
        db_user = self.user_repository.get_by_email(session,data.email)

        if db_user is None:
            raise HTTPException(
                status_code=401,
                detail="EMAIL_OR_PASSWORD_INVALID"
            )

        if not password_hash.verify(data.password,db_user.password_hash):
            raise HTTPException(
                status_code=401,
                detail="EMAIL_OR_PASSWORD_INVALID"
            ) 

        expires_at = datetime.now(timezone.utc) + timedelta(hours=30)

        refresh = create_refresh_token(db_user.id,expires_at)

        token = create_access_token(db_user.id)

        self.refresh_token_repository.create(
            session=session,
            token=RefreshToken(
                user_id=db_user.id,
                token_hash=hash_token(refresh),
                expires_at=expires_at,
                revoked=False
            )
        )

        return {"message": "Login realizado com sucesso",
                "access_token": token,
                "refresh_token": refresh,
                "token_type": "bearer",
                "user": {
                    "id": db_user.id,
                    "username": db_user.username,
                    "email": db_user.email
                }}

    def search_users(self,session: Session, username: str):
        if len(username) < 2:
            return []
        return self.user_repository.search_by_username(session,username)

    def refresh_token(
            self,
            session: Session,
            token: RefreshRequest
    ):
        pass