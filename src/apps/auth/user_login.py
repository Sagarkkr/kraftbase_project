from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.helpers import get_password_hash,authenticate_user
from src.apps.auth.schemas import User, UserInDB
from src.db import get_db

router = APIRouter()

@router.post("/signup")
def signup(user: User, db: Session = Depends(get_db)):
    existing_user = db.query(UserInDB).filter(UserInDB.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    hashed_password = get_password_hash(user.password)
    new_user = UserInDB(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@router.post("/login")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    request.session["user"] = user.username
    return {"message": "Login successful"}

@router.post("/logout")
def logout(request: Request):
    if "user" in request.session:
        del request.session["user"]
        return {"message": "Logout successful"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No user is logged in",
    )

@router.get("/profile")
def profile(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("user")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    user = db.query(UserInDB).filter(UserInDB.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return {"username": user.username}
