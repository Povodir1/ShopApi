from fastapi import APIRouter, status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.schemas.user import UserRegister, UserTokenDataSchema
from app.services.api_crud.user import create_user
from app.services.security import (create_access_token, is_unique_email, user_by_email_pass,
                                   is_correct_pass,code_ver,update_access_token,
                                   create_refresh_token,block_refresh_token,block_access_token,
                                   create_code,user_auth,get_token)

from app.services.emai_sender import send_email
from app.database import get_session
from sqlalchemy.orm.session import Session
from app.exceptions import InvalidDataError,ObjectAlreadyExistError

from app.database import auth_clients
import json


from app.database import access_blacklist_client,refresh_token_client
router = APIRouter(tags=["Auth"])


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          session: Session = Depends(get_session)
          ):

    user_data =  user_by_email_pass(form_data.username,form_data.password,session)
    new_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data.id)
    return {"access_token": new_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"}


@router.post("/logout")
def logout(token:str = Depends(user_auth),
           user:UserTokenDataSchema = Depends(get_token)
           ):
    block_access_token(token)
    block_refresh_token(user.id)
    return {"message": "Токен отозван (внесен в черный список)"}


@router.post("/refresh_token")
def new_access_token(refresh_token:str,
                     session: Session = Depends(get_session)
                     ):
    new_token = update_access_token(refresh_token,session)
    return {"access_token": new_token,
            "token_type": "bearer"}



@router.post("/register/request",status_code=status.HTTP_200_OK)
def request_code(user:UserRegister,
                 session:Session = Depends(get_session)
                 ):
    if not user.password == user.password_again:
        raise InvalidDataError("Пароли отличаются")
    if not is_unique_email(user.email,session):
        raise ObjectAlreadyExistError(detail="Пользователь с таким Email уже зарегестрирован")
    user.password = is_correct_pass(user.password)
    code = create_code(user.email,auth_clients,300,{"user": user.model_dump()})

    send_email(user.email,code,"Verify your account")
    return {"message":"Код подтверждения отправлен на email, отправте код на ./verify_code"}


@router.post("/register/confirm")
def verify_code(email:EmailStr,
                code:str,
                session:Session = Depends(get_session)
                ):
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
    user_data = UserTokenDataSchema(**new_user.model_dump())
    new_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data.id)
    return {"access_token": new_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"}
