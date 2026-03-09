import uuid
import time
from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
from pinecone.exceptions import PineconeException
from app.config.settings import settings

class VectorStoreError(Exception):
    pass

class VectorStore:
    def __init__(self):
        if not settings.PINECONE_API_KEY:
            raise VectorStoreError("PINECONE_API_KEY not configured")
        try:
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY, timeout=30)
            self.index_name = settings.PINECONE_INDEX_NAME
            self.dimension = settings.PINECONE_DIMENSION
            
            if self.dimension <= 0:
                raise VectorStoreError(f"Invalid PINECONE_DIMENSION: {self.dimension}")

            self._ensure_index_exists()
            self.index = self.pc.Index(self.index_name)
        except PineconeException as e:
            raise VectorStoreError(f"Pinecone connection error: {str(e)}")
        except Exception as e:
            error_msg = str(e)
            if "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
                raise VectorStoreError(f"Connection timeout to Pinecone API: {error_msg}")
            raise VectorStoreError(f"Error initializing vector store: {error_msg}")
    
    def _ensure_index_exists(self):
        try:
            # list all indexes : if not exists create one
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            if self.index_name not in existing_indexes:
                region = settings.PINECONE_ENVIRONMENT or "us-east-1"
                self.pc.create_index(name=self.index_name, dimension=self.dimension, metric="cosine", spec=ServerlessSpec(cloud="aws", region=region))
                
                # Timeout check (60 seconds)
                start_time = time.time()
                while not self.pc.describe_index(self.index_name).status['ready']:
                    if time.time() - start_time > 60:
                        raise VectorStoreError(f"Timeout waiting for index {self.index_name}")
                    time.sleep(1)
        except PineconeException as e:
            raise VectorStoreError(f"Error creating Pinecone index: {str(e)}")
    

    def upsert_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]], namespace: Optional[str] = None) -> int:
        """ insert chunks into the vector store"""
        # validation
        if not chunks or not embeddings:
            return 0
        if len(chunks) != len(embeddings):
            raise VectorStoreError("Number of chunks must match number of embeddings")
        
        vectors_to_upsert = []

        for chunk, embedding in zip(chunks, embeddings):
            if not embedding or len(embedding) != self.dimension:
                raise VectorStoreError(f"Embedding dimension mismatch. Expected {self.dimension}, got {len(embedding) if embedding else 0}")
            
            metadata = {"text": chunk.get("text", ""),
                        "chunk_index": chunk.get("chunk_index", 0), 
                        "source_file": chunk.get("source_file", ""), 
                        "start_char": chunk.get("start_char", 0), 
                        "end_char": chunk.get("end_char", 0)}

            if "page_number" in chunk:
                metadata["page_number"] = chunk["page_number"]
            if "file_hash" in chunk:
                metadata["file_hash"] = chunk["file_hash"]
                
            vectors_to_upsert.append({"id": str(uuid.uuid4()), "values": embedding, "metadata": metadata})
        # upsert vectors in batches of 100
        try:
            total_upserted = 0
            for i in range(0, len(vectors_to_upsert), 100):
                batch = vectors_to_upsert[i:i + 100]
                self.index.upsert(vectors=batch, namespace=namespace)
                total_upserted += len(batch)
            return total_upserted
        except PineconeException as e:
            raise VectorStoreError(f"Error upserting vectors: {str(e)}")
    

    def query(self, query_embedding: List[float], top_k: int = 5, namespace: Optional[str] = None, filter: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """ take the query embedding and
            search for the most similar vectors in the index"""
        # validation
        if not query_embedding or len(query_embedding) != self.dimension:
            raise VectorStoreError(f"Query embedding dimension mismatch. Expected {self.dimension}, got {len(query_embedding) if query_embedding else 0}")
        try:
            results = self.index.query(vector=query_embedding, top_k=top_k, namespace=namespace, filter=filter, include_metadata=True)
            matches = []
            for match in results.matches:
                # extract the source file and filename
                source_file = match.metadata.get("source_file", "")
                filename = source_file
                if "/" in source_file:
                    filename = source_file.split("/")[-1]
                elif "\\" in source_file:
                    filename = source_file.split("\\")[-1]
                # create match data
                match_data = {"id": match.id, 
                              "score": match.score, 
                              "text": match.metadata.get("text", ""), 
                              "source_file": source_file, 
                              "filename": filename, 
                              "chunk_index": match.metadata.get("chunk_index", 0)}
                              
                if "page_number" in match.metadata:
                    match_data["page_number"] = match.metadata["page_number"]
                if "file_hash" in match.metadata:
                    match_data["file_hash"] = match.metadata["file_hash"]
                matches.append(match_data)
            return matches
            
        except PineconeException as e:
            raise VectorStoreError(f"Error querying Pinecone: {str(e)}")

