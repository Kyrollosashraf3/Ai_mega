from fastapi import FastAPI, APIRouter, Depends
from app.config import settings

router = APIRouter( prefix="/chat" ,   tags=["chat"],)

@router.get("/")
async def hello():

    app_name = settings.APP_NAME
    app_version = settings.APP_VERSION
    return {
        "app_name": app_name,
        "app_version": app_version,
    }
