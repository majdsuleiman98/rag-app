from fastapi import FastAPI, APIRouter
import os

base_router = APIRouter(prefix="/api/v1", tags=["base"])

@base_router.get("/")
async def welcome_message():
    app_name = os.getenv("APP_NAME", "My Application")
    app_version = os.getenv("APP_VERSION", "1.0.0")
    return {"message": f"Welcome to the {app_name} API", "version": app_version}