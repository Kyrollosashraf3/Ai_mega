from fastapi import FastAPI, APIRouter, Depends
import os
from app.config.settings import settings

router = APIRouter( prefix="/helth" ,   tags=["V1"],)

@router.get("/")
#async def welcome(app_settings: Settings = Depends(Settings)):
async def welcome():
   
    app_name = settings.APP_NAME
    app_version = settings.APP_VERSION
    #app_name = "MEGA AI    "
    #app_version = "0.0.1 .."

    return {
        "app_name": app_name,
        "app_version": app_version,
    }
