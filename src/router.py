from fastapi import APIRouter
from src.apps.auth.router import auth_router
from src.apps.forms.router import form_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router, tags=['Auth'])
api_router.include_router(form_router, tags=['Form'])
