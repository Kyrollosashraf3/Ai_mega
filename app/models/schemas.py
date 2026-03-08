# =============================================================================
# REQUEST SCHEMAS
# =============================================================================

from pydantic import BaseModel
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
    stream: Optional[bool] = False