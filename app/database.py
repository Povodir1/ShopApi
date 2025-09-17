from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models.base import Base
engine = create_engine(settings.DB_URL,echo=True)


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

