from fastapi import APIRouter, HTTPException, status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserRegister, UserToken, UserLogin
from app.services.user import create_user, is_unique_email, user_by_email_pass
from app.services.security import create_token

router = APIRouter(tags=["auth"])

def token_json(tkn:str):
    return {"access_token": tkn,
            "token_type": "bearer"}

@router.post("/token")
def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = user_by_email_pass(form_data.username,form_data.password)
    new_token = create_token(user_data.model_dump())
    return token_json(new_token)


@router.post("/register")
def register(user:UserRegister):
    if not is_unique_email(user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Пользователь с таким Email уже зарегестрирован")
    new_user = create_user(user)
    user_data = UserToken(**new_user.model_dump())
    new_token = create_token(user_data.model_dump())
    return token_json(new_token)


@router.post("/login")
def login(user:UserLogin):
    user_data = user_by_email_pass(user.email, user.password_hash)
    new_token = create_token(user_data.model_dump())
    return token_json(new_token)