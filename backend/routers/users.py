from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schema import UserResponse
from models import User
from services.user import UserService
from database.database import get_session
from security.dependencies import get_current_user

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

user_service = UserService()

@router.get("/search", response_model=list[UserResponse])
async def search_users(
    username: str,
    session: Session = Depends(get_session),
    #O current_user serve só para ver se o usuário está autenticado
    current_user: User = Depends(get_current_user)
):
    return user_service.search_users(session,username)

