from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import WebSearchRequest, WebSearchResponse
from app.core.llm.perplexity import get_perplexity_client, PerplexityError, SearchMode
from app.config.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/web", tags=["Web Search"])

@router.post("/search", response_model=WebSearchResponse)
async def web_search(request: WebSearchRequest):
    """
    Dedicated endpoint for web search using Perplexity.
    """
    try:
        logger.info(f"[WebSearch] Query: {request.query} | Mode: {request.mode}")
        
        # Determine search mode
        search_mode = SearchMode.FAST if request.mode.lower() == "fast" else SearchMode.DEEP
        
        # Get perplexity client
        perplexity = get_perplexity_client()
        
        # Execute search
        search_result = perplexity.search(
            query=request.query,
            mode=search_mode,
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens
        )
        
        return WebSearchResponse(
            query=request.query,
            mode=request.mode,
            content=search_result.get("content", ""),
            citations=search_result.get("citations", [])
        )
        
    except PerplexityError as e:
        logger.error(f"[WebSearch] Perplexity error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search service error: {str(e)}")
    except Exception as e:
        logger.error(f"[WebSearch] Unexpected error: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
