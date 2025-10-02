from fastapi import APIRouter, HTTPException, status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.schemas.user import UserRegister, UserToken, UserLogin
from app.services.user import create_user, is_unique_email, user_by_email_pass, reset_password
from app.services.security import create_token,access_code
from app.services.emai_sender import send_email

from app.database import auth_clients,password_reset_client
import json

router = APIRouter(tags=["auth"])

def token_json(tkn:str):
    return {"access_token": tkn,
            "token_type": "bearer"}


def code_ver(data,code):
    try:
        stored_code = data.get("code")
        if str(stored_code) != str(code):
            raise ValueError("неверный код подтверждения")
    except Exception as e:
        raise e


def create_code(email:EmailStr,redis_db,ttl,new_data:dict|None = None):
    if not new_data:
        new_data = {}
    code = access_code()

    new_data["code"] = code
    new_data["try_counts"] = 3
    data = new_data
    data_json = json.dumps(data)
    if redis_db.exists(email):
        redis_db.delete(email)
    redis_db.setex(email, ttl, data_json)
    return code

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

@router.post("/register/request",status_code=status.HTTP_200_OK)
def request_code(user:UserRegister):
    if not is_unique_email(user.email):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь с таким Email уже зарегестрирован")
    code = create_code(user.email,auth_clients,300,{"user": user.model_dump()})

    send_email(user.email,code,"Verify your account")
    return {"message":"Код подтверждения отправлен на email, отправте код на ./verify_code"}


@router.post("/register/confirm")
def verify_code(email:EmailStr,code:str):

    data_json = auth_clients.get(email)

    try:
        data = json.loads(data_json)
        if not data_json:
            raise ValueError("Код не найден или истек срок действия")
        #
        if data.get("try_counts") ==0:
            auth_clients.delete(email)
            raise ValueError("Код больше не действителен")
        data["try_counts"] -= 1
        auth_clients.set(email, json.dumps(data))
        #
        code_ver(data,code)
        user_data = data.get("user")
        auth_clients.delete(email)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{e}"
        )
    new_user = create_user(UserRegister(**user_data))
    user_data = UserToken(**new_user.model_dump())
    new_token = create_token(user_data.model_dump())
    return token_json(new_token)

@router.post("/reset_password/request")
def forgot_password(email:EmailStr):
    code = create_code(email, password_reset_client, 600, )
    send_email(email, code, "Change password")
    return {"message": "Код подтверждения отправлен на email, отправте код на ./verify_code"}

@router.post("/reset_password/verify")
def verify_code_for_pass(email:EmailStr,code:str):
    data_json = password_reset_client.get(email)
    try:
        data = json.loads(data_json)
        if data.get("try_counts") ==0:
            password_reset_client.delete(email)
            raise ValueError("Код больше не действителен")
        data["try_counts"] -= 1
        password_reset_client.set(email, json.dumps(data))
        code_ver(data, code)
        return {"msg":"go to '/reset_password/confirm' to confirm new password"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{e}]")

@router.post("/reset_password/confirm")
def confirm_pass(email:EmailStr,code:str,new_password:str):
    data_json = password_reset_client.get(email)
    try:
        code_ver(data_json,code)
        reset_password(email, new_password)
        password_reset_client.delete(email)
        return {"Msg":"Пароль изменен"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{e}"
        )


@router.post("/login")
def login(user:UserLogin):
    user_data = user_by_email_pass(user.email, user.password_hash)
    new_token = create_token(user_data.model_dump())
    return token_json(new_token)