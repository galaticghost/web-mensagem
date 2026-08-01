from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session

from database.database import get_session
from services.user import UserService
from schema.user import UserLogin, UserCreate

user_service = UserService()

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

@router.post("/login",status_code=status.HTTP_200_OK)
async def login(
    data: UserLogin,
    session: Session = Depends(get_session)
):
    return user_service.login(session,data)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: UserCreate,
    session: Session = Depends(get_session)
    ):
    return user_service.register(session,data)
    