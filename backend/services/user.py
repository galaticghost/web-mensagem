from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt

from repository import UserRepository,RefreshTokenRepository
from models import User, RefreshToken
from security.jwt import create_access_token,create_refresh_token,hash_token,decode_token
from schema import UserCreate,UserLogin,LoginResponse,UserResponse, RefreshResponse

password_hash = PasswordHash.recommended()

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.refresh_token_repository = RefreshTokenRepository()


    """
    Verifica se o email ou nome de usuário já existem no banco.
    Senão existirem é criado um novo usuário.
    """
    def register(self, session: Session, data: UserCreate):
        if self.user_repository.get_by_email(session,data.email) is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="EMAIL_ALREADY_EXISTS"
                )
        
        if self.user_repository.get_by_username(session,data.username) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="USERNAME_ALREADY_EXISTS"
            )
    
        user = User(
            username=data.username,
            email=data.email,
            password_hash=password_hash.hash(data.password)
        )
    
        self.user_repository.create(session,user)
        return {"message": "Usuário criado com sucesso"}

    """
    Valida se o usuário existe e se a senha está certa.
    Em seguida cria um token de acesso e de refresh e os retorna junto ao usuário.
    """
    def login(self, session: Session, data:UserLogin) -> LoginResponse:
        db_user = self.user_repository.get_by_email(session,data.email)

        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="EMAIL_OR_PASSWORD_INVALID"
            )

        if not password_hash.verify(data.password,db_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="EMAIL_OR_PASSWORD_INVALID"
            )

        expires_at = datetime.now(timezone.utc) + timedelta(hours=30)

        access_token, refresh_token = self._create_token_pair(db_user.id, expires_at)

        self.refresh_token_repository.create(
            session=session,
            token=RefreshToken(
                user_id=db_user.id,
                token_hash=hash_token(refresh_token),
                expires_at=expires_at,
                revoked=False
            )
        )

        return LoginResponse(
                message="LOGIN_SUCCESS",
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
                user=UserResponse(
                    id=db_user.id,
                    username=db_user.username,
                    email=db_user.email
                )
            )

    def logout(
            self,
            session: Session,
            refresh_token: str,
    ):
        token_hash = hash_token(refresh_token)
        
        stored_token = self.refresh_token_repository.get_by_hash(
            session=session,
            token_hash=token_hash
        )

        if stored_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID_TOKEN"
            )

        if stored_token.revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="TOKEN_REVOKED"
            )

        self.refresh_token_repository.revoke(
            session=session,
            token=stored_token
        )

        return {
            "message": "LOGOUT_SUCCESS"
        } 

    def search_users(self,session: Session, username: str) -> list[User]:
        if len(username) < 2:
            return []
        return self.user_repository.search_by_username(session,username)

    def refresh_token(
            self,
            session: Session,
            token: str
    ) -> RefreshResponse:

        payload = self._validate_refresh_token(token)

        token_hash = hash_token(token)

        stored_token = self.refresh_token_repository.get_by_hash(
            session=session,
            token_hash=token_hash
        )

        if stored_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID_TOKEN"
            )

        if stored_token.revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="TOKEN_REVOKED"
            )

        if stored_token.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="TOKEN_EXPIRED"
            )

        user_id = int(payload.sub)

        if stored_token.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID_USER"
            )

        self.refresh_token_repository.revoke(
            session=session,
            token=stored_token
        )

        expires_at = datetime.now(timezone.utc) + timedelta(hours=30)

        access_token, new_refresh_token = self._create_token_pair(user_id,expires_at)

        self.refresh_token_repository.create(
            session=session,
            token=RefreshToken(
                user_id=user_id,
                token_hash=hash_token(new_refresh_token),
                expires_at=expires_at,
                revoked=False
            )
        )

        return RefreshResponse(
            access_token=access_token,
            token_type="bearer",
            refresh_token=new_refresh_token
        )

    """
    Cria um par de tokens (access e refresh).
    """
    @staticmethod
    def _create_token_pair(
            user_id: int,
            expires_at: datetime
    ) -> tuple[str,str]:
        access_token = create_access_token(user_id)

        refresh_token = create_refresh_token(user_id,expires_at)

        return access_token, refresh_token

    def _validate_refresh_token(
            self,
            refresh_token: str
    ):
        try:
            payload = decode_token(refresh_token)
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="TOKEN_EXPIRED"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID_TOKEN"
            )

        if payload.type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID_TOKEN_TYPE"
            )
