from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from models import User
from schema.user import UserCreate,UserLogin
from database.database import get_session
from security.jwt import create_access_token
from repository.user import UserRepository

password_hash = PasswordHash.recommended()

user_repository = UserRepository()

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

@router.post("/login",status_code=status.HTTP_200_OK)
async def login(
    user: UserLogin,
    session: Session = Depends(get_session)
):
    db_user = user_repository.get_by_email(session,user.email)

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )

    if not password_hash.verify(user.password,db_user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        ) 

    token = create_access_token({
        "sub": str(db_user.id)
    })

    return {"message": "Login realizado com sucesso",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": db_user.id,
                "username": db_user.username,
                "email": db_user.email
            }}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user: UserCreate,
    session: Session = Depends(get_session)
    ):

    if user_repository.get_by_email(session,user.email) is not None:
        raise HTTPException(
            status_code=409,
            detail="Já existe um usuário cadastrado com esse email"
        )

    if user_repository.get_by_username(session,user.username) is not None:
        raise HTTPException(
            status_code=409,
            detail="Já existe um usuário cadastrado com esse nome de usuário"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=password_hash.hash(user.password)
    )

    user_repository.create(session,new_user)
    return {"message": "Usuário criado com sucesso"}