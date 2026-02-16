"""
Mega AI Agent - Main FastAPI Application
Production-ready AI agent with RAG, memory, and chat history.
"""
from fastapi import FastAPI, Request, status
#from fastapi.middleware.cors import CORSMiddleware
#from fastapi.responses import JSONResponse
#from fastapi.exceptions import RequestValidationError
from app.config.logger import get_logger

from app.routes.base import router as home_router
from app.routes.chat import router as chat_router
from app.routes.data import router as file_router


#logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="MEGA" ,
    version="0.0.1",
    description="Mega AI Agent - Production-ready AI with RAG, Memory, and Chat History"
)

app.include_router(home_router)
app.include_router(chat_router)
app.include_router(file_router)