from app.database import db_session
from app.models.user import User
from app.schemas.user import UserSchema, UserRegister
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

