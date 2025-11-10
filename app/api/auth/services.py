import datetime

from app.api.users.schemas import UserTokenDataSchema, UserSchema

from pydantic import EmailStr

from app.models.user import User
from app.core.exceptions import ObjectNotFoundError,InvalidDataError
from app.core.security import verify_pass,hash_pass


def is_unique_email(email:EmailStr,session):
    user = session.query(User).filter(User.email == email).first()
    return False if user else True


def user_by_email_pass(email:str|EmailStr,password:str,session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        raise ObjectNotFoundError("Нет пользователя с таким email")
    if not verify_pass(password,user.password_hash):
        raise InvalidDataError("Неверный пароль")
    user.last_login = datetime.datetime.now()
    return UserTokenDataSchema(id = user.id,name = user.name,role = user.roles.name,currency=user.currency.name,language=user.language.name)


def reset_password(email:EmailStr|str,new_password,session):
    user = session.query(User).filter(User.email == email).first()
    user.password_hash = hash_pass(new_password)
    session.flush()
    return UserSchema.model_validate(user,from_attributes=True)

