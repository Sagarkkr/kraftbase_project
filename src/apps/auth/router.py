from fastapi import APIRouter
from src.apps.auth import user_login

auth_router = APIRouter(prefix="/auth")
auth_router.include_router(user_login.router)
