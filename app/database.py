from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models.base import Base
import redis

engine = create_engine(settings.DB_URL)


SessionLocal = sessionmaker(bind=engine)

@contextmanager
def db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
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

