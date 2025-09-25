from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_URL: str
    JWT_SECRET_KEY: str
    EMAIL_SENDER:str
    EMAIL_PASSWORD:str

settings = Settings()