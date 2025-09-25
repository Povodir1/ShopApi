from fastapi import APIRouter, HTTPException, status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.schemas.user import UserRegister, UserToken, UserLogin
from app.services.user import create_user, is_unique_email, user_by_email_pass
from app.services.security import create_token,access_code
from app.services.emai_sender import send_email

router = APIRouter(tags=["auth"])

def token_json(tkn:str):
    return {"access_token": tkn,
            "token_type": "bearer"}

@router.post("/token")
def token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user_data = user_by_email_pass(form_data.username,form_data.password)
        new_token = create_token(user_data.model_dump())
        return token_json(new_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

redis_like_db = {}

###############################

@router.post("/request_code",status_code=status.HTTP_200_OK)
def request_code(user:UserRegister):
    if not is_unique_email(user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Пользователь с таким Email уже зарегестрирован")
    code = access_code()
    redis_like_db[user.email] = user,code

    send_email(user.email,code,"Verify your account")
    return {"message":"Код подтверждения отправлен на email, отправте код на ./verify_code"}


@router.post("/verify_code")
def verify_code(email:EmailStr,code:str):
    # сравнить и найти юзера
    print(redis_like_db)
    if redis_like_db[email][1] != code:
        # исправить код ошибки
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Неверный код")
    user = redis_like_db[email][0]
    redis_like_db.pop(email)

    new_user = create_user(user)
    user_data = UserToken(**new_user.model_dump())
    new_token = create_token(user_data.model_dump())
    return token_json(new_token)



@router.post("/login")
def login(user:UserLogin):
    user_data = user_by_email_pass(user.email, user.password_hash)
    new_token = create_token(user_data.model_dump())
    return token_json(new_token)