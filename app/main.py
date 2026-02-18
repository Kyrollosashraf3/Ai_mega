"""
Mega AI Agent - Main FastAPI Application
Production-ready AI agent with RAG, memory, and chat history.
"""
from fastapi import FastAPI, Request, status
#from fastapi.middleware.cors import CORSMiddleware
#from fastapi.responses import JSONResponse
#from fastapi.exceptions import RequestValidationError

from app.routes.base import router as home_router
from app.routes.chat import router as chat_router
from app.routes.data import router1 as file_router
from app.routes.data import router2 as data_process_router

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

from app.config import get_logger
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="MEGA" ,
    version="0.0.1",
    description="Mega AI Agent - Production-ready AI with RAG, Memory, and Chat History"
)


# just start app -> call MongoDB client
@app.on_event("startup")
async def startup_db_client():
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()



app.include_router(home_router)
app.include_router(chat_router)
app.include_router(file_router)
app.include_router(data_process_router)