from sqlalchemy import Column, String
from pydantic import BaseModel

class UserInDB(BaseModel):
    __tablename__ = "users"
    username: str
    email: str | None = None
    password: str

class User(BaseModel):
    username: str
    email: str | None = None
    password: str