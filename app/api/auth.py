from fastapi import APIRouter, HTTPException, status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.schemas.user import UserRegister, UserToken, UserLogin
from app.services.user import create_user, is_unique_email, user_by_email_pass
from app.services.security import create_token,access_code
from app.services.emai_sender import send_email

from app.database import client
import json
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


@router.post("/request_code",status_code=status.HTTP_200_OK)
def request_code(user:UserRegister):
    if not is_unique_email(user.email):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь с таким Email уже зарегестрирован")
    code = access_code()

    data = {
        "user": user.model_dump(),
        "code": code
    }
    data_json = json.dumps(data)
    if client.exists(user.email):
        client.delete(user.email)
    client.setex(user.email,300,data_json)

    send_email(user.email,code,"Verify your account")
    return {"message":"Код подтверждения отправлен на email, отправте код на ./verify_code"}


@router.post("/verify_code")
def verify_code(email:EmailStr,code:str):

    data_json = client.get(email)

    if not data_json:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Код не найден или истек срок действия"
        )

    try:

        data = json.loads(data_json)
        stored_code = data.get("code")
        user_data = data.get("user")


        if str(stored_code) != str(code):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,  # Более подходящий код ошибки
                detail="Неверный код подтверждения"
            )

        client.delete(email)
    except Exception as e:
        raise e
    new_user = create_user(UserRegister(**user_data))
    user_data = UserToken(**new_user.model_dump())
    new_token = create_token(user_data.model_dump())
    return token_json(new_token)




@router.post("/login")
def login(user:UserLogin):
    user_data = user_by_email_pass(user.email, user.password_hash)
    new_token = create_token(user_data.model_dump())
    return token_json(new_token)