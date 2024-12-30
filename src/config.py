from decouple import config
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_NAME : str = config("DB_NAME")
    DB_PASSWORD : str = config("DB_PASSWORD")
    DB_USER : str = config("DB_USER")

settings = Settings()
