
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
import redis

from app.core.config import settings

from app.models.base import Base


engine = create_engine(settings.DB_URL)

SessionLocal = sessionmaker(bind=engine,class_=Session)

def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def create_clear_db():
    Base.metadata.create_all(engine)

def delete_db():
    Base.metadata.drop_all(engine)

auth_clients = redis.Redis(host=settings.REDIS_HOST,
                     port = settings.REDIS_PORT,
                     db = 0,
                     decode_responses=settings.REDIS_IS_DECODE)

password_reset_client = redis.Redis(host=settings.REDIS_HOST,
                     port = settings.REDIS_PORT,
                     db = 1,
                     decode_responses=settings.REDIS_IS_DECODE)

refresh_token_client = redis.Redis(host=settings.REDIS_HOST,
                     port = settings.REDIS_PORT,
                     db = 2,
                     decode_responses=settings.REDIS_IS_DECODE)

access_blacklist_client = redis.Redis(host=settings.REDIS_HOST,
                     port = settings.REDIS_PORT,
                     db = 3,
                     decode_responses=settings.REDIS_IS_DECODE)




