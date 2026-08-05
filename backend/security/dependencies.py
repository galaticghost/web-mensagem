from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from repository.user import UserRepository
from database.database import get_session
from security.jwt import decode_token

#Serve para pegar o token de acesso do json do token original 
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login" # Isso daqui é apenas para o docs do fastapi
)

user_repository = UserRepository()

def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session),
    ):
    
    try:
        payload = decode_token(token)
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
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="INVALID_TOKEN"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="INVALID_TOKEN"
        )

    user = user_repository.get_by_id(session, int(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="USER_NOT_FOUND"
        )

    return user

def get_user_from_token(
        session: Session,
        token: str
):
    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

    user_id = payload.get("sub")

    if user_id is None:
        return None

    user = user_repository.get_by_id(session, int(user_id))
    
    return user