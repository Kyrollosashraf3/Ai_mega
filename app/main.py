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
from app.routes.logs import router as logs_router
from app.routes.rag import router as rag_router
from app.routes.web_search import router as web_search_router


from app.routes.data import file_router 
from app.routes.data import data_process_router 
from app.routes.data import data_delete_router 

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.db import ProjectModel, AssetModel, chunkModel

from app.config import get_logger
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="MEGA_AI" ,
    version="0.0.2",
    description="Production-ready AI with Chat, Web Search, RAG, MongoDB, and Pinecone "
)


# just start app -> call MongoDB client
@app.on_event("startup")
async def startup_db_client():
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

    # Initialize collections and indexes
    # await ProjectModel.create_instance(app.db_client)
    # await AssetModel.create_instance(app.db_client)
    # await chunkModel.create_instance(app.db_client)

    #logger.info("MongoDB connected and collections initialized.")


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()



app.include_router(home_router)
app.include_router(chat_router)
app.include_router(web_search_router)
app.include_router(file_router)
app.include_router(data_process_router)
app.include_router(rag_router)
app.include_router(data_delete_router)
app.include_router(logs_router)
