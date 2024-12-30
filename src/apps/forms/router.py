from fastapi import APIRouter
from src.apps.forms import forms_api

form_router = APIRouter(prefix="/form")
form_router.include_router(forms_api.router)
