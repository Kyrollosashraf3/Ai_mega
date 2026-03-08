from typing import Dict, Any, Optional
from enum import Enum
from perplexity import Perplexity, DefaultHttpxClient
import httpx

from app.config.settings import settings
from app.config.logger import get_logger

logger = get_logger(__name__)


class SearchMode(str, Enum):
    """Search modes: fast (sonar) or deep (sonar-pro)"""
    FAST = "fast"
    DEEP = "deep"


class PerplexityError(Exception):
    """Perplexity API error"""
    pass


class PerplexityClient:
    """Perplexity AI web search client with retry logic."""
    
    MODELS = {
        SearchMode.FAST: "sonar",
        SearchMode.DEEP: "sonar-pro"
    }
    
    def __init__(self):
        if not settings.PERPLEXITY_API_KEY:
            raise PerplexityError("PERPLEXITY_API_KEY not configured")
        
        timeout_config = httpx.Timeout(connect=5.0, read=60.0, write=10.0, pool=10.0)
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100, keepalive_expiry=30.0)
        
        try:
            self.client = Perplexity(
                api_key=settings.PERPLEXITY_API_KEY,
                max_retries=3,
                timeout=timeout_config,
                http_client=DefaultHttpxClient(limits=limits, verify=True, http2=True)
            )
        except Exception:
            self.client = Perplexity(
                api_key=settings.PERPLEXITY_API_KEY,
                max_retries=3,
                timeout=timeout_config,
                http_client=DefaultHttpxClient(limits=limits, verify=True)
            )
    
    def search(
        self, 
        query: str, 
        mode: SearchMode = SearchMode.FAST,
        timeout: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """Perform web search and return structured results with citations."""
        if not query or not query.strip():
            raise PerplexityError("Query cannot be empty")
        
        model = self.MODELS[mode]
        final_temperature = temperature if temperature is not None else 0.2
        final_top_p = top_p if top_p is not None else 0.9
        final_max_tokens = max_tokens if max_tokens is not None else 1024
        
        try:
            client = self.client.with_options(timeout=httpx.Timeout(timeout)) if timeout else self.client
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful search assistant. Provide comprehensive, accurate answers based on current web search results. Always cite your sources with specific URLs."
                    },
                    {"role": "user", "content": query}
                ],
                temperature=final_temperature,
                top_p=final_top_p,
                max_tokens=final_max_tokens
            )
            
            content = response.choices[0].message.content or "" if response.choices else ""
            
            citations = []
            if hasattr(response, 'citations') and response.citations:
                try:
                    citations = list(response.citations)
                except:
                    pass
            
            images = []
            if hasattr(response, 'images') and response.images:
                try:
                    images = list(response.images)
                except:
                    pass
            
            usage = {}
            if hasattr(response, 'usage') and response.usage:
                try:
                    usage = {
                        "prompt_tokens": getattr(response.usage, 'prompt_tokens', 0),
                        "completion_tokens": getattr(response.usage, 'completion_tokens', 0),
                        "total_tokens": getattr(response.usage, 'total_tokens', 0)
                    }
                except:
                    pass
            
            return {
                "success": True,
                "content": content,
                "citations": citations,
                "images": images,
                "model": model,
                "mode": mode.value,
                "usage": usage,
                "query": query
            }
            
        except Exception as e:
            error_msg = str(e)
            
            if "401" in error_msg or "Unauthorized" in error_msg:
                logger.error(f"[Perplexity] Invalid API key")
                raise PerplexityError("Invalid Perplexity API key")
            elif "429" in error_msg or "Rate limit" in error_msg:
                logger.error(f"[Perplexity] Rate limit exceeded")
                raise PerplexityError("Rate limit exceeded")
            elif "timeout" in error_msg.lower():
                logger.error(f"[Perplexity] Request timeout")
                raise PerplexityError(f"Request timeout: {error_msg}")
            elif "connection" in error_msg.lower():
                logger.error(f"[Perplexity] Connection error")
                raise PerplexityError(f"Connection error: {error_msg}")
            else:
                logger.error(f"[Perplexity] {type(e).__name__}: {error_msg}")
                raise PerplexityError(f"Search error: {error_msg}")


_perplexity_client = None


def get_perplexity_client() -> PerplexityClient:
    """Get or create singleton PerplexityClient instance."""
    global _perplexity_client
    if _perplexity_client is None:
        _perplexity_client = PerplexityClient()
    return _perplexity_client
