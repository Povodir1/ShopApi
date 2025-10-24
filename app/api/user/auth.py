from fastapi import APIRouter, HTTPException, status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.schemas.user import UserRegister, UserSchema, UserLogin
from app.services.api_crud.user import create_user
from app.services.security import create_token,access_code, is_unique_email, user_by_email_pass,reset_password,is_correct_pass,code_ver
from app.services.emai_sender import send_email
from app.database import get_session
from sqlalchemy.orm.session import Session
from app.exceptions import InvalidDataError

from app.database import auth_clients,password_reset_client
import json

router = APIRouter(tags=["Auth"])

def token_json(tkn:str):
    return {"access_token": tkn,
            "token_type": "bearer"}


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
def token(form_data: OAuth2PasswordRequestForm = Depends(),session:Session = Depends(get_session)):
    user_data =  user_by_email_pass(form_data.username,form_data.password,session)
    new_token =  create_token(user_data)
    return token_json(new_token)


@router.post("/register/request",status_code=status.HTTP_200_OK)
def request_code(user:UserRegister,session:Session = Depends(get_session)):
    if not is_unique_email(user.email,session):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь с таким Email уже зарегестрирован")
    user.password_hash = is_correct_pass(user.password_hash)
    code = create_code(user.email,auth_clients,300,{"user": user.model_dump()})

    send_email(user.email,code,"Verify your account")
    return {"message":"Код подтверждения отправлен на email, отправте код на ./verify_code"}


@router.post("/register/confirm")
def verify_code(email:EmailStr,code:str,session:Session = Depends(get_session)):

    data_json = auth_clients.get(email)


    data = json.loads(data_json)
    if not data_json:
        raise InvalidDataError("Код не найден или истек срок действия")
    #
    if data.get("try_counts") ==0:
        auth_clients.delete(email)
        raise InvalidDataError("Код больше не действителен")
    data["try_counts"] -= 1
    auth_clients.set(email, json.dumps(data))
    #
    code_ver(data,code)
    user_data = data.get("user")
    auth_clients.delete(email)
    new_user = create_user(UserRegister(**user_data),session)
    user_data = UserSchema(**new_user.model_dump())
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
    data = json.loads(data_json)
    if data.get("try_counts") ==0:
        password_reset_client.delete(email)
        raise InvalidDataError("Код больше не действителен")
    data["try_counts"] -= 1
    password_reset_client.set(email, json.dumps(data))
    code_ver(data, code)
    return {"msg":"go to '/reset_password/confirm' to confirm new password"}

@router.post("/reset_password/confirm")
def confirm_pass(email:EmailStr,code:str,new_password:str = Depends(is_correct_pass),session:Session = Depends(get_session)):
    data_json = password_reset_client.get(email)

    data = json.loads(data_json)
    code_ver(data,code)
    reset_password(email, new_password,session)
    password_reset_client.delete(email)
    return {"Msg":"Пароль изменен"}



@router.post("/login")
def login(user:UserLogin,session:Session = Depends(get_session)):
    user_data = user_by_email_pass(user.email, user.password_hash,session)
    new_token = create_token(user_data)
    return token_json(new_token)
