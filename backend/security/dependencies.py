from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from repository.user import UserRepository
from database.database import get_session
from security.jwt import decode_access_token

#Serve para pegar o token de acesso do json do token original 
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login" # Isso daqui é apenas para o docs do fastapi
)

user_repository = UserRepository()

def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session),
    ):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    user = user_repository.get_by_id(session, int(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado"
        )

    return user

def get_user_from_token(
        session: Session,
        token: str
):
    payload = decode_access_token(token)

    if payload is None:
        return None

    user_id = payload.get("sub")

    if user_id is None:
        return None

    user = user_repository.get_by_id(session, int(user_id))
    
    return user