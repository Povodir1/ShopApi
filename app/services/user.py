
from app.database import db_session
from app.models.user import User
from app.schemas.user import UserSchema, UserRegister, UserPatch
from pydantic import EmailStr

def is_unique_email(email:EmailStr):
    with db_session() as session:
        data = [el[0] for el in session.query(User.email).all()]
        return False if email in data else True


def get_user(user_id):
    with db_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        return UserSchema.model_validate(user)

def create_user(user_data: UserRegister):
    user = User(**user_data.model_dump())
    with db_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return UserSchema.model_validate(user)

def patch_user(user_id:int, new_data:UserPatch):
    with db_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        for key,value in new_data.model_dump(exclude_none=True).items():
            setattr(user,key,value)
        session.commit()
        session.refresh(user)
        return UserSchema.model_validate(user)

