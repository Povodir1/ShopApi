from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

class Settings(BaseSettings):
    DB_URL: str
    JWT_SECRET_KEY: str
    EMAIL_SENDER:str
    EMAIL_PASSWORD:str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_IS_DECODE:bool
    MEDIA_PATH:Path = Path(__file__).resolve().parent.parent/"media"

settings = Settings()