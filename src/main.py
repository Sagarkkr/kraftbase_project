from fastapi import FastAPI
#Local imports
from src.db import Base, engine
from src.middleware import CustomSessionMiddleware
from src.router import api_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(CustomSessionMiddleware, secret_key="supersecretkey")

app.include_router(api_router)
