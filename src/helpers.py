from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.apps.auth.schemas import User, UserInDB


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str) -> UserInDB:
    user = db.query(UserInDB).filter(UserInDB.username == username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None