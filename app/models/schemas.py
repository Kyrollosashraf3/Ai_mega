# =============================================================================
# REQUEST SCHEMAS
# =============================================================================

from pydantic import BaseModel, Field
from typing import Optional , List

class ProcessRequest(BaseModel):
    file_id: str = None
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_reset: Optional[int] = 0


class MessageItem(BaseModel):
    role: str
    content: str
    
class ChatRequest(BaseModel):
    model: str
    messages: List[MessageItem]
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0
    max_tokens: Optional[int] = 1024
    
    web_search_mode: Optional[str] = None
    web_search_max_tokens: Optional[int] = None
    web_search_temperature: Optional[float] = None
    web_search_top_p: Optional[float] = None
    stream: Optional[bool] = False


    
class ChunkSearchRequest(BaseModel):
    query: str = Field(..., description="Search query text")
    project_id: str = Field(..., description="Project ID")
    file_ids: Optional[List[str]] = Field(None, description="List of filenames or file hashes")
    top_k: int = Field(3, ge=1, le=50, description="Number of chunks to retrieve")

class ChunkSearchResponse(BaseModel):
    query: str
    top_k: int
    num_results: int
    file_filter_applied: bool
    filtered_files: Optional[List[str]] = None
    chunks: List[dict]

class WebSearchRequest(BaseModel):
    query: str = Field(..., description="The search query for Perplexity")
    mode: Optional[str] = Field("fast", description="Search mode: 'fast' or 'deep'")
    max_tokens: Optional[int] = Field(1024, description="Maximum tokens for the response")
    temperature: Optional[float] = Field(0.2, description="Sampling temperature")
    top_p: Optional[float] = Field(0.9, description="Top-p sampling")

class WebSearchResponse(BaseModel):
    query: str
    mode: str
    content: str
    citations: List[str] = []