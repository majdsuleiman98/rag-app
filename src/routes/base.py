from fastapi import APIRouter, Depends
from helpers.config import get_settings, Settings

base_router = APIRouter(prefix="/api/v1", tags=["base"])

@base_router.get("/")
async def welcome_message(app_settings: Settings = Depends(get_settings)):
    # app_settings = get_settings()
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {"message": f"Welcome to the {app_name} API", "version": app_version}