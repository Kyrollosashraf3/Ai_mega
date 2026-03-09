from typing import List, Dict, Any, Optional
from app.core.rag.embeddings import generate_embedding, EmbeddingError
from app.vectordb import VectorStore, VectorStoreError
from app.config.logger import get_logger

logger = get_logger(__name__)


class RetrievalError(Exception):
    pass


class RetrievalService:
    """Service for retrieving document chunks and augmenting queries with context."""
    
    def __init__(self):
        try:
            self.vector_store = VectorStore()
            logger.debug("[Retrieval Service] Vector store initialized")
        except VectorStoreError as e:
            logger.error(f"[Retrieval Service] Failed to initialize vector store: {str(e)}")
            raise RetrievalError(f"Failed to initialize vector store: {str(e)}")
    
    def retrieve_context(
        self, 
        query: str, 
        project_id: str,
        top_k: int = 5,
        file_ids: Optional[List[str]] = None,
        filter: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant document chunks for given query.
        
        Args:
            query: The search query
            project_id: The project ID (used as Pinecone namespace)
            top_k: Number of results to return
            file_ids: Optional list of asset names (source_file) to filter by
            filter: Additional metadata filters
        """
        if not query or not query.strip():
            raise RetrievalError("Query cannot be empty")
        
        try:
            logger.debug(f"[Retrieval Service] Generating embedding for query: {query[:50]}...")
            query_embedding = generate_embedding(query)
        except EmbeddingError as e:
            logger.error(f"[Retrieval Service] Embedding generation failed: {str(e)}")
            raise RetrievalError(f"Failed to generate query embedding: {str(e)}")
        
        # Build filter
        query_filter = filter or {}
        
        # In this project, file_ids are asset_names, stored as "source_file" in Pinecone metadata
        if file_ids:
            valid_file_ids = [fid for fid in file_ids if fid]
            if valid_file_ids:
                if len(valid_file_ids) == 1:
                    query_filter["source_file"] = {"$eq": valid_file_ids[0]}
                else:
                    query_filter["source_file"] = {"$in": valid_file_ids}
        
        try:
            logger.debug(f"[Retrieval Service] Querying vector store for project: {project_id}")
            results = self.vector_store.query(
                query_embedding=query_embedding,
                top_k=top_k,
                namespace=project_id,
                filter=query_filter if query_filter else None
            )
            logger.info(f"[Retrieval Service] Found {len(results)} matches for project {project_id}")
            return results
        except VectorStoreError as e:
            logger.error(f"[Retrieval Service] Vector store query failed: {str(e)}")
            raise RetrievalError(f"Failed to query vector store: {str(e)}")
    

def get_retrieval_service() -> RetrievalService:
    """Factory function to get RetrievalService instance."""
    return RetrievalService()
