from fastapi import APIRouter,Depends
from pydantic import EmailStr

from app.services.security import reset_password,is_correct_pass,code_ver
from app.services.emai_sender import send_email
from app.database import get_session
from sqlalchemy.orm.session import Session
from app.exceptions import InvalidDataError
from app.services.security import create_code

from app.database import password_reset_client
import json

router = APIRouter(tags=["Auth"])



@router.post("/reset_password/request")
def forgot_password(email:EmailStr):
    code = create_code(email, password_reset_client, 600, )
    send_email(email, code, "Change password")
    return {"message": "Код подтверждения отправлен на email, отправте код на ./verify"}

@router.post("/reset_password/verify")
def verify_code_for_pass(email:EmailStr,
                         code:str
                         ):
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
def confirm_pass(email:EmailStr,code:str,
                 new_password:str = Depends(is_correct_pass),
                 session:Session = Depends(get_session)
                 ):
    data_json = password_reset_client.get(email)
    data = json.loads(data_json)
    code_ver(data,code)
    reset_password(email, new_password,session)
    password_reset_client.delete(email)
    return {"Msg":"Пароль изменен"}