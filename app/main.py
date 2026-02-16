"""
Mega AI Agent - Main FastAPI Application
Production-ready AI agent with RAG, memory, and chat history.
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.config.logger import get_logger


logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="ff" ,
    version="1.0.0",
    description="Mega AI Agent - Production-ready AI with RAG, Memory, and Chat History"
)
