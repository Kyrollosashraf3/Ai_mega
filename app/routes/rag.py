import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from typing import List, Optional
from app.config.logger import get_logger
from app.core.rag.retrieval import get_retrieval_service, RetrievalError
from app.models import ChunkSearchRequest, ChunkSearchResponse

router = APIRouter(prefix="/rag", tags=["RAG"])
logger = get_logger(__name__)

@router.post("/search", response_model=ChunkSearchResponse)
async def search_document_chunks(request: ChunkSearchRequest, fastapi_request: Request):
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if request.top_k < 1 or request.top_k > 50:
            raise HTTPException(status_code=400, detail="top_k must be between 1 and 50")
       
        from app.db.project_model import ProjectModel
        project_model = await ProjectModel.create_instance(db_client=fastapi_request.app.db_client)
        project = await project_model.get_project(project_id=request.project_id)

        retrieval_service = get_retrieval_service()
        chunks = retrieval_service.retrieve_context(query=request.query, 
                                                    project_id=str(project.id),
                                                    top_k=request.top_k, 
                                                    file_ids=request.file_ids)
        
        logger.info(f"[Search] Completed")
        
        return ChunkSearchResponse( query=request.query, 
                                    top_k=request.top_k, 
                                    num_results=len(chunks), 
                                    file_filter_applied=bool(request.file_ids), 
                                    filtered_files=request.file_ids, 
                                    chunks=chunks)

    except RetrievalError as e:
        logger.error(f"[Search] Retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Retrieval error: {str(e)}")
    except Exception as e:
        logger.error(f"[Search] Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

