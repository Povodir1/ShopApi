

from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserRegister
from app.services.user import create_user, is_unique_email


router = APIRouter(tags=["auth"])


@router.post("/token")
def get_token():
    pass


@router.post("/register")
def register(user:UserRegister):
    if not is_unique_email(user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Пользователь с таким Email уже зарегестрирован")
    return create_user(user)


@router.post("/login")
def login():
    pass