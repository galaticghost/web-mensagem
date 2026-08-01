from fastapi import HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from repository.user import UserRepository
from models import User
from security.jwt import create_access_token
from schema.user import UserCreate,UserLogin

password_hash = PasswordHash.recommended()

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register(self, session: Session, data: UserCreate):
        if self.user_repository.get_by_email(session,data.email) is not None:
                raise HTTPException(
                    status_code=409,
                    detail="Já existe um usuário cadastrado com esse email"
                )
        
        if self.user_repository.get_by_username(session,data.username) is not None:
            raise HTTPException(
                status_code=409,
                detail="Já existe um usuário cadastrado com esse nome de usuário"
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
                detail="Email ou senha inválidos"
            )

        if not password_hash.verify(data.password,db_user.password_hash):
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

    def search_users(self,session: Session, username: str):
        if len(username) < 2:
            return []
        return self.user_repository.search_by_username(session,username)
